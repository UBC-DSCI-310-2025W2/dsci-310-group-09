.PHONY: all clean

PYTHONPATH=.
export PYTHONPATH

all: reports/online-shoppers-classification.html

#Step1, download raw data from URL to csv in data folder
data/raw_online_shoppers.csv: source/01_download_raw_data.py
	python source/01_download_raw_data.py

#Step2, OHE to categorical variables and data cleaning
data/processed_online_shoppers.csv results/online_shoppers_class_balance.csv: source/02_data_cleaning.py data/raw_online_shoppers.csv
	python source/02_data_cleaning.py \
	"data/raw_online_shoppers.csv" \
	"data/processed_online_shoppers.csv"

#Step3, Save EDA histogram plot to results/
results/online_shoppers_eda_histograms.png: source/03_EDA_histogram.py data/processed_online_shoppers.csv
	python source/03_EDA_histogram.py \
	"data/processed_online_shoppers.csv" \
	"results/online_shoppers_eda_histograms.png"

#Step4, output of randomforest
results/online_shoppers_model_classification_report.csv results/online_shoppers_model_auc.csv results/online_shoppers_model_feature_importance.png results/online_shoppers_model_shap_summary.png: source/04_model_output.py data/processed_online_shoppers.csv
	python source/04_model_output.py \
	"data/processed_online_shoppers.csv" \
	"results/online_shoppers_model"

reports/online-shoppers-classification.html: reports/online-shoppers-classification.qmd \
	data/processed_online_shoppers.csv \
	results/online_shoppers_class_balance.csv \
	results/online_shoppers_eda_histograms.png \
	results/online_shoppers_model_classification_report.csv \
	results/online_shoppers_model_auc.csv \
	results/online_shoppers_model_feature_importance.png \
	results/online_shoppers_model_shap_summary.png
	quarto render reports/online-shoppers-classification.qmd

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
.PHONY: all clean