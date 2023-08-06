from prose import FitsManager

fm = FitsManager("/Users/lgrcia/data/RAW_Callisto_20210927_Sp2315-0627_I+z", depth=2)
i = 16
files = fm.observation_files(i, show=False)

from prose import Sequence, blocks, Image

ref_path = files["images"][len(files["images"])//2]
ref = Image(ref_path)

calibs = files.copy()
del calibs["images"]
calib_block = blocks.Calibration(**calibs)

from prose import Sequence, blocks, Image

ref_path = files["images"][len(files["images"])//2]
ref = Image(ref_path)

calibration = Sequence([
    calib_block,
    blocks.Trim(),
    blocks.SegmentedPeaks(n_stars=150),
    blocks.detection.LimitStars(min=3),
    blocks.Cutouts(),
    blocks.MedianPSF(),
    blocks.Moffat2D(),
])

calibration.run(ref, show_progress=False)

from prose.sequence import MPSequence

photometry = Sequence([
    calib_block,
    blocks.Trim(),
    blocks.SegmentedPeaks(n_stars=15),
    blocks.detection.LimitStars(min=3),
    blocks.Cutouts(),
    blocks.MedianPSF(),
    blocks.Moffat2D(),
    blocks.Twirl(ref.stars_coords),
    blocks.Set(stars_coords=ref.stars_coords),
    blocks.AffineTransform(data=False, inverse=True),
    blocks.centroids.Quadratic(),
    blocks.PhotutilsAperturePhotometry(scale=ref.fwhm),
    blocks.Peaks(),
    blocks.Del("data", "cutouts"),
])

photometry.run(files["images"])