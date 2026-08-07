# Aviation Tool

Find airport weather and distances to other airports within a time range

#### Download the latest release or build it yourself:

## Clone [aviation-tool](https://github.com/rainbowardite/aviation-tool.git)

## Get Data
Get `airports.csv`, `countries.csv`, and `runways.csv` from [ourairports.com](https://ourairports.com/data/) and place them in the `/files` folder

## Run:
### Terminal
`python ./aviation-tool.py`

### exe [Windows Only (I think?)]

#### Build exe

##### Terminal
`python -m PyInstaller .\aviation-tool.spec`

##### Batch File
run batch file at `\update_executable.bat`

#### Run exe
exe outputs to `dist\aviation-tool.exe`
