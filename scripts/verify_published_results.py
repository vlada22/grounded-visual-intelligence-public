from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "web" / "data" / "evidence.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"PUBLIC RESULT VERIFICATION FAILED\n- {message}")


def close(actual: float, expected: float, name: str, tolerance: float = 1e-9) -> None:
    require(math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance), f"{name}: expected {expected}, got {actual}")


def decode_rle(mask: dict) -> bytearray:
    height = int(mask["height"])
    width = int(mask["width"])
    total = height * width
    decoded = bytearray(total)
    position = 0
    value = 0
    for count in mask["counts"]:
        count = int(count)
        require(count >= 0, "RLE contains a negative run")
        end = position + count
        require(end <= total, "RLE run exceeds mask bounds")
        if value:
            decoded[position:end] = b"\x01" * count
        position = end
        value = 1 - value
    require(position == total, f"RLE length mismatch: decoded {position} of {total} pixels")
    return decoded


def mask_iou(left: bytearray, right: bytearray) -> float:
    require(len(left) == len(right), "matched masks have different sizes")
    intersection = 0
    union = 0
    for a, b in zip(left, right):
        intersection += int(bool(a and b))
        union += int(bool(a or b))
    require(union > 0, "matched masks have empty union")
    return intersection / union


def bbox_iou(left: dict, right: dict) -> float:
    x0 = max(float(left["xMin"]), float(right["xMin"]))
    y0 = max(float(left["yMin"]), float(right["yMin"]))
    x1 = min(float(left["xMax"]), float(right["xMax"]))
    y1 = min(float(left["yMax"]), float(right["yMax"]))
    intersection = max(0.0, x1 - x0) * max(0.0, y1 - y0)
    area_left = max(0.0, float(left["xMax"]) - float(left["xMin"])) * max(0.0, float(left["yMax"]) - float(left["yMin"]))
    area_right = max(0.0, float(right["xMax"]) - float(right["xMin"])) * max(0.0, float(right["yMax"]) - float(right["yMin"]))
    union = area_left + area_right - intersection
    require(union > 0, "matched bounding boxes have empty union")
    return intersection / union


def mask_centroid_x(mask: dict, decoded: bytearray) -> float:
    width = int(mask["width"])
    xs = 0.0
    count = 0
    for index, value in enumerate(decoded):
        if value:
            xs += index % width
            count += 1
    require(count > 0, "mask is empty")
    return xs / count


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    video = payload["video"]
    answer = payload["answer"]
    comparison = payload["comparison"]
    models = payload["models"]

    sam2 = models["groundedSam2"]["frames"]
    sam3 = models["sam3"]["frames"]
    frame_count = int(video["frameCount"])
    require(len(sam2) == frame_count == len(sam3), "model frame counts do not match video.frameCount")
    require([frame["frameIndex"] for frame in sam2] == list(range(frame_count)), "Grounded SAM 2 frame indices are not contiguous")
    require([frame["frameIndex"] for frame in sam3] == list(range(frame_count)), "SAM 3 frame indices are not contiguous")

    mask_ious: list[float] = []
    bbox_ious: list[float] = []
    decoded_by_model: dict[str, list[bytearray]] = {"groundedSam2": [], "sam3": []}
    for left_frame, right_frame in zip(sam2, sam3):
        close(float(left_frame["timestamp"]), float(right_frame["timestamp"]), "matched frame timestamp")
        left_mask = decode_rle(left_frame["mask"])
        right_mask = decode_rle(right_frame["mask"])
        decoded_by_model["groundedSam2"].append(left_mask)
        decoded_by_model["sam3"].append(right_mask)
        mask_ious.append(mask_iou(left_mask, right_mask))
        bbox_ious.append(bbox_iou(left_frame["bbox"], right_frame["bbox"]))

    close(statistics.fmean(mask_ious), float(comparison["meanMaskIou"]), "mean mask IoU")
    close(statistics.median(mask_ious), float(comparison["medianMaskIou"]), "median mask IoU")
    close(min(mask_ious), float(comparison["minimumMaskIou"]), "minimum mask IoU")
    close(max(mask_ious), float(comparison["maximumMaskIou"]), "maximum mask IoU")
    require(mask_ious.index(min(mask_ious)) == int(comparison["minimumMaskIouFrame"]), "minimum mask IoU frame does not match")
    close(statistics.fmean(bbox_ious), float(comparison["meanBoundingBoxIou"]), "mean bounding-box IoU")
    require(int(comparison["matchedFrames"]) == frame_count, "comparison.matchedFrames does not match video.frameCount")

    last_a, first_b = map(int, answer["boundaryFrames"])
    require(first_b == last_a + 1, "published transition boundary is not between adjacent sampled frames")
    close(float(sam3[last_a]["timestamp"]), float(answer["lastObservedInASeconds"]), "last observed in A timestamp")
    close(float(sam3[first_b]["timestamp"]), float(answer["firstObservedInBSeconds"]), "first observed in B timestamp")
    close(float(answer["resolutionSeconds"]), 1.0 / float(video["fps"]), "sampling resolution")

    zones = {zone["id"]: zone for zone in payload["zones"]}
    width = float(video["width"])
    for model_key, frames in (("groundedSam2", sam2), ("sam3", sam3)):
        left_x = mask_centroid_x(frames[last_a]["mask"], decoded_by_model[model_key][last_a]) / width
        right_x = mask_centroid_x(frames[first_b]["mask"], decoded_by_model[model_key][first_b]) / width
        require(zones["A"]["xMin"] <= left_x <= zones["A"]["xMax"], f"{model_key} boundary frame {last_a} centroid is not in zone A")
        require(zones["B"]["xMin"] <= right_x <= zones["B"]["xMax"], f"{model_key} boundary frame {first_b} centroid is not in zone B")

    print("Article 01 published-result verification passed")
    print(f"frames={frame_count} transition={answer['lastObservedInASeconds']:.2f}s->{answer['firstObservedInBSeconds']:.2f}s mean_mask_iou={statistics.fmean(mask_ious):.6f}")


if __name__ == "__main__":
    main()
