cd /home/co/git/RegulatoryComplexity/320_experiments_results


//
// clean submissions file
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

save master.dta, replace
outsheet using master.csv, delimiter(",") replace

use master.dta, clear
keep id_student total_score
duplicates drop

hist total_score, ///
	freq bin(9) ///
	title("Distribution of number of correct answers")
graph export "hist_scores.png", replace

use master.dta, replace

