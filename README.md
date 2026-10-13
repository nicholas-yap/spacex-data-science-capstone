# SpaceX Data Science Capstone

IBM Applied Data Science Capstone by Nicholas Yap.

## Presentation and analysis

- [Completed presentation](ds-capstone-completed.pptx)
- [API snapshot and data validation](notebooks/01-data-collection.ipynb)
- [Web scraping](notebooks/jupyter-labs-webscraping.ipynb)
- [Wrangling and EDA](notebooks/02-wrangling-eda.ipynb)
- [SQL analysis](notebooks/jupyter-labs-eda-sql-coursera_sqllite.ipynb)
- [Folium maps](notebooks/03-interactive-maps.ipynb)
- [Classification](notebooks/SpaceX-Machine-Learning-Prediction-Part-5-v1.ipynb)
- [Dash dashboard](spacex_dashboard.py)

## Main results

The modeling dataset contains 90 Falcon 9 launches from 4 June 2010 to 5 November 2020. It has 60 Class 1 outcomes (66.7%). KSC LC 39A has the highest observed site rate at 17/22 (77.3%); CCAFS SLC 40 contributes the largest number of Class 1 outcomes, 33.

Saved classification notebook results: logistic regression, SVM, decision tree and KNN each achieve 83.33% on 18 test launches. The tree has the highest 10-fold CV score at 87.68%. Its confusion matrix is `[[3, 3], [0, 12]]` (actual rows, predicted columns). The test baseline that always predicts Class 1 is 66.67%.

## Data scope and limitations

- `dataset_part_1.csv` and `dataset_part_2.csv`: 90 enriched course records. Payload mass is already mean-imputed.
- `dataset_part_3.csv`: the 90-by-83 encoded feature matrix.
- `Spacex.csv`: a separate 101-row SQL snapshot.
- `spacex_web_scraped.csv`: 121 rows from Wikipedia revision 1027686922 (June 2021).
- `API_call_spacex_api.json`: archived API response provided with the course. The new collection notebook inspects this response and validates the enriched course CSV; it does not claim a fresh API extraction.

Class 1 includes `True Ocean` (five controlled ocean outcomes), as well as ASDS and RTLS successes. It should not be interpreted as the number of recovered reusable boosters. Class 0 includes failures, missing outcomes and no attempts. Mission success in the SQL source is a different label.

The supplied classification lab fits StandardScaler before train/test splitting. These are the saved course results, not a leakage-free production evaluation. A subsequent evaluation should use preprocessing inside training folds, remove information unavailable at prediction time (including potentially cumulative reuse fields), and hold out a later period. Small test and orbit/site groups limit conclusions. The decision tree uses random_state=2 in the saved notebook.

Map distances are approximate Haversine distances to manually selected coastline, road and rail points, not nearest-feature measurements or safety clearances. OpenStreetMap tiles require internet access and retain their attribution.

## Run locally

```bash
pip install -r requirements.txt
python spacex_dashboard.py
```

Open `http://127.0.0.1:8051`. The site dropdown updates the pie chart. The payload range updates the scatter plot. Booster block provides the color grouping.

```bash
python build_maps.py
python -m http.server 8052
```

Open the HTML files under `http://127.0.0.1:8052/maps/`. GitHub shows HTML source, so download or serve the repository to interact with maps. Run notebooks from the repository root or `notebooks/`. The bootstrap cell resolves the data directory. Original saved analytical outputs are retained; the three new companion notebooks include executed outputs. The original course notebooks may attempt to refresh data online before falling back to cached files.

## Sources

Course data: IBM DS0321EN Skills Network, `https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/`.

API: https://api.spacexdata.com/v4/launches/past

Wikipedia snapshot: https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922

Map attribution: https://www.openstreetmap.org/copyright

Presentation artwork and course notebook instructions retain their original IBM/Coursera attribution. Dataset and course content rights remain with their respective owners.
