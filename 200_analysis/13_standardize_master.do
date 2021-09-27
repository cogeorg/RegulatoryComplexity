cd /home/co/git/RegulatoryComplexity/200_analysis

insheet using ../020_auxiliary_data/Sections/Protected_list/Master_standardized.csv, delimiter(";") clear
	rename v1 key
	rename v2 key_cons
	rename v3 category
	
	drop key
	duplicates drop key_cons, force
	
	sort key_cons
	
	drop if key_cons == ""
outsheet using ../020_auxiliary_data/Sections/Protected_list/Master_consolidated.csv, delimiter(";") replace
