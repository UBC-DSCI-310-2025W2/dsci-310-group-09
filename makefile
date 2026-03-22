.PHONY: all clean

all: reports/online-shoppers-classification.html

#Step1, download raw data from URL to csv in data folder
data/raw_online_shoppers.csv: source/01_download_raw_data.py
	python source/01_download_raw_data.py \
	"https://archive.ics.uci.edu/ml/machine-learning-databases/00468/online_shoppers_intention.csv" \
	"data/raw_online_shoppers.csv"

#Step2, OHE to categorical variables and data cleaning
data/processed_online_shoppers.csv results/online_shoppers_class_balance.csv: source/02_data_cleaning.py data/raw_online_shoppers.csv
	python source/02_data_cleaning.py \
	"data/raw_online_shoppers.csv" \
	"data/processed_online_shoppers.csv"

#Step3, Save EDA histogram plot to results/
results/online_shoppers_eda_histograms.png: source/03_EDA_histogram.py data/processed_online_shoppers.csv
	python source/03_create_online_shoppers_eda.py \
	"data/processed_online_shoppers.csv" \
	"results/online_shoppers_eda_histograms.png"

#Step4, output of randomforest
results/online_shoppers_model_classification_report.csv results/online_shoppers_model_auc.csv results/online_shoppers_model_feature_importance.png results/online_shoppers_model_shap_summary.png: source/04_model_output.py data/processed_online_shoppers.csv
	python source/04_model_output.py \
	"data/processed_online_shoppers.csv" \
	"results/online_shoppers_model"

clean:
	rm -f data/raw_online_shoppers.csv
	rm -f data/processed_online_shoppers.csv
	rm -f results/online_shoppers_class_balance.csv
	rm -f results/online_shoppers_eda_histograms.png
	rm -f results/online_shoppers_model_classification_report.csv
	rm -f results/online_shoppers_model_auc.csv
	rm -f results/online_shoppers_model_feature_importance.png
	rm -f results/online_shoppers_model_shap_summary.png
.PHONY: all clean

all: reports/online-shoppers-classification.html

# Step 1: download raw data
data/raw_online_shoppers.csv: source/01_download_raw_data.py
	python source/01_download_raw_data.py \
		"https://archive.ics.uci.edu/ml/machine-learning-databases/00468/online_shoppers_intention.csv" \
		"data/raw_online_shoppers.csv"

# Step 2: clean data and save class balance summary
data/processed_online_shoppers.csv results/online_shoppers_class_balance.csv: source/02_data_cleaning.py data/raw_online_shoppers.csv
	python source/02_data_cleaning.py \
		"data/raw_online_shoppers.csv" \
		"data/processed_online_shoppers.csv"

# Step 3: create EDA histogram figure
results/online_shoppers_eda_histograms.png: source/03_EDA_histogram.py data/processed_online_shoppers.csv
	python source/03_EDA_histogram.py \
		"data/processed_online_shoppers.csv" \
		"results/online_shoppers_eda_histograms.png"

# Step 4: train model and save outputs
results/online_shoppers_model_classification_report.csv \
results/online_shoppers_model_auc.csv \
results/online_shoppers_model_feature_importance.png \
results/online_shoppers_model_shap_summary.png: source/04_model_output.py data/processed_online_shoppers.csv
	python source/04_model_output.py \
		"data/processed_online_shoppers.csv" \
		"results/online_shoppers_model"

# Step 5: render Quarto report
reports/online-shoppers-classification.html: \
	reports/online-shoppers-classification.qmd \
	reports/citations.bib \
	data/processed_online_shoppers.csv \
	results/online_shoppers_class_balance.csv \
	results/online_shoppers_eda_histograms.png \
	results/online_shoppers_model_classification_report.csv \
	results/online_shoppers_model_auc.csv \
	results/online_shoppers_model_feature_importance.png \
	results/online_shoppers_model_shap_summary.png
	quarto render reports/online-shoppers-classification.qmd --to html

clean:
	rm -f data/raw_online_shoppers.csv
	rm -f data/processed_online_shoppers.csv
	rm -f results/online_shoppers_class_balance.csv
	rm -f results/online_shoppers_eda_histograms.png
	rm -f results/online_shoppers_model_classification_report.csv
	rm -f results/online_shoppers_model_auc.csv
	rm -f results/online_shoppers_model_feature_importance.png
	rm -f results/online_shoppers_model_shap_summary.png
	rm -f reports/online-shoppers-classification.html