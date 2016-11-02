from flask import request, jsonify, redirect, url_for,flash,  render_template, request, session, abort
from views import app


@app.route('/title_1_Y')
def title_1_Y():
    return render_template('PreClass/TITLE I--FINANCIAL STABILITY.html')

@app.route('/title_2_Y')
def title_2_Y():
    return render_template('PreClass/TITLE II--ORDERLY LIQUIDATION AUTHORITY.html')

@app.route('/title_3_Y')
def title_3_Y():
    return render_template('PreClass/TITLE III--TRANSFER OF POWERS TO THE COMPTROLLER OF THE CURRENCY, THE CORPORATION, AND THE BOARD OF GOVERNORS.html')

@app.route('/title_4_Y')
def title_4_Y():
    return render_template('PreClass/TITLE IV--REGULATION OF ADVISERS TO HEDGE FUNDS AND OTHERS.html')

@app.route('/title_5_Y')
def title_5_Y():
    return render_template('PreClass/TITLE V--INSURANCE.html')

@app.route('/title_6_Y')
def title_6_Y():
    return render_template('PreClass/TITLE VI--IMPROVEMENTS TO REGULATION OF BANK AND SAVINGS ASSOCIATION HOLDING COMPANIES AND DEPOSITORY INSTITUTIONS.html')

@app.route('/title_7_Y')
def title_7_Y():
    return render_template('PreClass/TITLE VII--WALL STREET TRANSPARENCY AND ACCOUNTABILITY.html')

@app.route('/title_8_Y')
def title_8_Y():
    return render_template('PreClass/TITLE VIII--PAYMENT, CLEARING, AND SETTLEMENT SUPERVISION.html')

@app.route('/title_9_Y')
def title_9_Y():
    return render_template('PreClass/TITLE IX--INVESTOR PROTECTIONS AND IMPROVEMENTS TO THE REGULATION OF SECURITIES.html')

@app.route('/title_10_Y')
def title_10_Y():
    return render_template('PreClass/TITLE X--BUREAU OF CONSUMER FINANCIAL PROTECTION.html')

@app.route('/title_11_Y')
def title_11_Y():
    return render_template('PreClass/TITLE XI--FEDERAL RESERVE SYSTEM PROVISIONS.html')

@app.route('/title_12_Y')
def title_12_Y():
    return render_template('PreClass/TITLE XII--IMPROVING ACCESS TO MAINSTREAM FINANCIAL INSTITUTIONS.html')

@app.route('/title_13_Y')
def title_13_Y():
    return render_template('PreClass/TITLE XIII--PAY IT BACK ACT.html')

@app.route('/title_14_Y')
def title_14_Y():
    return render_template('PreClass/TITLE XIV--MORTGAGE REFORM AND ANTI-PREDATORY LENDING ACT.html')

@app.route('/title_15_Y')
def title_15_Y():
    return render_template('PreClass/TITLE XV--MISCELLANEOUS PROVISIONS.html')

@app.route('/title_16_Y')
def title_16_Y():
    return render_template('PreClass/TITLE XVI--SECTION 1256 CONTRACTS.html')





@app.route('/title_1')
def title_1():
    return render_template('Original/TITLE I--FINANCIAL STABILITY.html')

@app.route('/title_2')
def title_2():
    return render_template('Original/TITLE II--ORDERLY LIQUIDATION AUTHORITY.html')

@app.route('/title_3')
def title_3():
    return render_template('Original/TITLE III--TRANSFER OF POWERS TO THE COMPTROLLER OF THE CURRENCY, THE CORPORATION, AND THE BOARD OF GOVERNORS.html')

@app.route('/title_4')
def title_4():
    return render_template('Original/TITLE IV--REGULATION OF ADVISERS TO HEDGE FUNDS AND OTHERS.html')

@app.route('/title_5')
def title_5():
    return render_template('Original/TITLE V--INSURANCE.html')

@app.route('/title_6')
def title_6():
    return render_template('Original/TITLE VI--IMPROVEMENTS TO REGULATION OF BANK AND SAVINGS ASSOCIATION HOLDING COMPANIES AND DEPOSITORY INSTITUTIONS.html')

@app.route('/title_7')
def title_7():
    return render_template('Original/TITLE VII--WALL STREET TRANSPARENCY AND ACCOUNTABILITY.html')

@app.route('/title_8')
def title_8():
    return render_template('Original/TITLE VIII--PAYMENT, CLEARING, AND SETTLEMENT SUPERVISION.html')

@app.route('/title_9')
def title_9():
    return render_template('Original/TITLE IX--INVESTOR PROTECTIONS AND IMPROVEMENTS TO THE REGULATION OF SECURITIES.html')

@app.route('/title_10')
def title_10():
    return render_template('Original/TITLE X-- BUREAU OF CONSUMER FINANCIAL PROTECTION.html')

@app.route('/title_11')
def title_11():
    return render_template('Original/TITLE XI--FEDERAL RESERVE SYSTEM PROVISIONS.html')

@app.route('/title_12')
def title_12():
    return render_template('Original/TITLE XII--IMPROVING ACCESS TO MAINSTREAM FINANCIAL INSTITUTIONS.html')

@app.route('/title_13')
def title_13():
    return render_template('Original/TITLE XIII--PAY IT BACK ACT.html')

@app.route('/title_14')
def title_14():
    return render_template('Original/TITLE XIV-- MORTGAGE REFORM AND ANTI-PREDATORY LENDING ACT.html')

@app.route('/title_15')
def title_15():
    return render_template('Original/TITLE XV--MISCELLANEOUS PROVISIONS.html')


@app.route('/title_16')
def title_16():
    return render_template('Original/TITLE XVI--SECTION 1256 CONTRACTS.html')
