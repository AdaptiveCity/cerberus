# Diff Detector

## diff_basic

This is a debug program to diff a background image (empty LT1) from an input image (occupied LT1).

The DiffBasic algorithm:
* measures the 'brightness' of the input image and adjusts (`cv2.convertScaleAbs`) the brightness of the 'empty' image to match it.
* subtracts the two images (`absDiff`)
* displays the resulting image as grayscale

## DiffBoxes

* Creates the grayscale absDiff image same as `diff_basic`
* Loads seat_boxes.json
* For each box in boxes.json the DiffBoxes thresholds the brightness of diff image to determine an 'occipied' status for that seat.

## Example `seat_boxes.json` created by `seat_boxes.html`
```
{
  "input_image": { "name": "lt1_empty_2592x1944.jpg",
                   "width": 2592,
                   "height": 1944
  },
  "points": [
    { "seat_id":  "ma7", "index": 0, "x": 1171, "y": 1745, "width": 201, "height": 194 },
    { "seat_id":  "ma8", "index": 1, "x": 1400, "y": 1753, "width": 212, "height": 182 },
    { "seat_id":  "ma9", "index": 2, "x": 1642, "y": 1729, "width": 200, "height": 206 },
    { "seat_id":  "ma10", "index": 3, "x": 1869, "y": 1735, "width": 187, "height": 204 },
    ...
  ]
}
```

## Run examples

Directory `~/LT1_imagesx` contains images of LT1 occupied.

```
source venv/bin/activate
cd diff_detector
python diff_boxes.py -i ~/LT1_imagesx/lt1_1.jpg -e lt1_empty.jpg -b 30 -j seat_boxes.json
```

```
python diff_basic.py -i ~/LT1_imagesx/lt1_1.jpg -e ~/LT1_imagesx/lt1_empty.jpg -b 30
```
