cd /home/co/git/RegulatoryComplexity/320_experiments_results


//
// clean user file
//
insheet using users.csv, clear delimiter(",")
	rename v1 id 
	rename v2 username
	rename v3 email
	rename v4 id_student
	rename v5 sex
	rename v6 ed_level
	rename v7 ed_yr_obtained
	rename v8 ed_area 
	rename v9 ed_institution
	rename v10 ex_area
	rename v11 ex_yr

	drop if email == "email"
	drop if username == "emile" | username == "co" | username == "co2" | username == "JEC" | username == "JEC2" | username == "JEC3" | username == "testaccount" | id <= 11

	keep id_student sex ed* ex*
	drop if sex == ""
	duplicates drop

save "users.dta", replace


//
// clean submissions file
//
insheet using submissions.csv, clear delimiter(",")

	// prepare variables
	rename v1 id
	rename studentid id_student
	rename question id_question
	rename regulation id_regulation
	gen double time = clock(substr(timetaken, 1, 8), "hms") 
	format time %tcHH:MM:ss 
	drop timetaken

	// some cleanup
	drop if answer == "Practice"
	destring answer, replace
	drop if id_student == "1234567" | id_student == "213" | id_student == "01440812" | id_student == "007"
	sort id_student
	drop if id_student == "11111"

// match with user data
merge m:1 id_student using users.dta
	keep if _merge == 3
	drop _merge

	drop id

	// some sorting
	sort id_student id_question

	// compute num right answers
	bysort id_student: egen total_score = max(score)
	gen is_correct = 0
	replace is_correct = 1 if answer == correctanswer

save master-1.dta, replace
outsheet using master-1.csv, delimiter(",") replace

//
// distribution of correct answers
//
use master-1.dta, clear
	keep id_student total_score
	duplicates drop

	hist total_score, ///
		freq bin(9) ///
		title("Distribution of number of correct answers")
graph export "hist_scores.png", replace


//
// prepare matching
//
insheet using reg_matching.csv, clear
	drop id_tmp
save reg_matching.dta, replace


//
// prepare measures
//
insheet using measures.csv, clear
	rename name id_orig_file
merge 1:1 id_orig_file using reg_matching.dta 
	keep if _merge == 3
	drop _merge
save measures.dta, replace

//
// finalize master data
//
use master-1.dta, replace
merge m:1 id_regulation using measures.dta
	keep if _merge == 3
	drop _merge
	egen id_user = group(user)

	scatter time level, ///
	title("Time vs Level")
graph export "scat_timelevel.png", replace

	scatter time totalvolume, ///
	title("Time vs Total Volume")
graph export "scat_timetotvol.png", replace

	scatter time potentialvolume, ///
	title("Time vs Potential Volume")
graph export "scat_timepotvol.png", replace

// regressions
areg time level, a(id_user)
areg time totalvolume, a(id_user)
areg time potentialvolume, a(id_user)

probit is_correct i.id_user level
probit is_correct i.id_user totalvolume
probit is_correct i.id_user potentialvolume


save master.dta, replace
