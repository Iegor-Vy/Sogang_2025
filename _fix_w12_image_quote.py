from pathlib import Path

path = Path(r"2026\Fall\Research Method of Data Science\W12\W12_RMDS.Rmd")
source = path.read_text(encoding="utf-8")
source = source.replace('src=data:image', 'src="data:image')
path.write_text(source, encoding="utf-8")
