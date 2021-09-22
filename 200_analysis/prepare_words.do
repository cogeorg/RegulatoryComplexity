clear

cd /home/co/git/RegulatoryComplexity/020_auxiliary_data/Sections/Protected_list

foreach varname in EconomicOperands Attributes  FunctionWords LegalReferences LogicalConnectors Other RegulatoryOperators {
	insheet using "words.csv", clear tab
	rename v1 word
	rename v2 class
	drop if word == "Word"
	keep if class == "`varname'"
	drop class
	save `varname'.dta, replace

	insheet using `varname'.txt, clear tab
	rename v1 word
	append using `varname'.dta, force
	duplicates drop
	sort word
	outsheet using `varname'.txt, replace non noq
}



cd /Users/co/git/RegulatoryComplexity/200_analysis/50_results
insheet using word_count.csv, delimiter(";") clear
	drop file_name
	correl
	gen id_title = _n

	
//
// NEW 2021-09-19
//
use Attributes.dta, clear
use EconomicOperands.dta, clear
