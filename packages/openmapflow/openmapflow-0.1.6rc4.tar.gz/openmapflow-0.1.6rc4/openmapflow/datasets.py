from openmapflow.labeled_dataset_existing import ExistingLabeledDataset

geowiki_landcover_2017 = ExistingLabeledDataset(
    dataset="geowiki_landcover_2017",
    source=(
        "Linda See. A global reference database of crowdsourced cropland data collected using the "
        + "Geo-Wiki platform, 2017."
    ),
    label_type="binary",
    license="CC BY-3.0",
    country="global",
    download_url="https://storage.googleapis.com/harvest-public-assets/openmapflow/datasets/crop/geowiki_landcover_2017.csv",
    source_code_url="https://github.com/nasaharvest/crop-mask/blob/master/datasets.py",
)

togo_crop_2019 = ExistingLabeledDataset(
    country="Togo",
    dataset="Togo_2019",
    download_url="https://storage.googleapis.com/harvest-public-assets/openmapflow/datasets/crop/Togo_2019.csv",
    label_type="binary",
    license="CC BY-4.0",
    source=(
        "Hannah Kerner, Gabriel Tseng, Inbal Becker-Reshef, Catherine Nakalembe, "
        + " Brian Barker, Blake Munshell, Madhava Paliyam, and Mehdi Hosseini. Rapid response "
        + "crop maps in data sparse regions. In ACM SIGKDD Conference on Data Mining and "
        + "Knowledge Discovery Workshops, 2020."
    ),
    source_code_url="https://github.com/nasaharvest/crop-mask/blob/master/datasets.py",
)

kenya_crop_2018_2019 = ExistingLabeledDataset(
    country="Kenya",
    dataset="Kenya_2018_2019",
    label_type="binary",
    license="CC BY-4.0",
    download_url="https://storage.googleapis.com/harvest-public-assets/openmapflow/datasets/crop/Kenya_2018_2019.csv",
    source_code_url="https://github.com/nasaharvest/crop-mask/blob/master/datasets.py",
)


datasets = [geowiki_landcover_2017, togo_crop_2019, kenya_crop_2018_2019]
