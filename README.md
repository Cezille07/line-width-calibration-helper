# line-width-calibration-helper

Generates an SVG you can print to verify your fountain pen nib width.

Initial layout based on this resource on [fountainpennetwork.com](): [Hi Res Nib Widths Chart](https://www.fountainpennetwork.com/forum/files/file/8-high-res-nib-widths-chart/). The file appears to be JPEG which introduced some artifacts. This coding exercise attempts to generate an SVG with price outputs for definitive measurement. 

## Running

Python 3 is required.

```python generate_nib_chart.py```

The output is an SVG file `nib_width_calibration_a4.svg`. Open it in a browser (tested on Edge), and print at 100% scale for A4 (more paper sizes coming soon).
