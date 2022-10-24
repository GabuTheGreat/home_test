import pandas as pd
from datetime import date

today = date.today()
# mm/dd/y
d3 = today.strftime("%d/%m/%y")
print("d3 =", d3)

#Read in the data
dd = pd.read_csv("~/Documents/challanges/home_test/analytics_specialist_hiring_dataset_final.csv")

#Calculating PAR(Portfolio at Risk) Status.
#subset the to remain with the key columns for PAR calculation
#** Do the calculation later on the main dataframe **####
par_dd = dd[["contract_reference", "status", "start_date", "end_date", "next_contract_payment_due_date"]]
#Format the date columns 
par_dd[["start_date", "end_date", "next_contract_payment_due_date"]] = par_dd[["start_date", "end_date", "next_contract_payment_due_date"]].apply(pd.to_datetime)
#Add a column for todays date
par_dd['today'] = pd.to_datetime(today)

#Calculate the difference in day
par_dd['Difference'] = (par_dd['today'] - par_dd['next_contract_payment_due_date']).dt.days

#Format date inputs to look presentable
par_dd['start_date'] = par_dd['start_date'].dt.strftime('%d/%m/%y')
par_dd['end_date'] = par_dd['end_date'].dt.strftime('%d/%m/%y')
par_dd['next_contract_payment_due_date'] = par_dd['next_contract_payment_due_date'].dt.strftime('%d/%m/%y')
par_dd['today'] = par_dd['today'].dt.strftime('%d/%m/%y')


#write function to calaculate PAR
def par (difference_in_days):
    if difference_in_days < 0:
        par = "On Time"
        
    elif 0 <= difference_in_days <= 7:
        par = "PAR0-7"
        
    elif 8 <= difference_in_days <= 30:
        par = "PAR8-30"
        
    elif 31 <= difference_in_days <= 90:
        par = "PAR31-90"
        
    elif difference_in_days >= 91:
        par = "PAR90+"
    
    return par

par_dd['PAR'] = par_dd['Difference'].apply(par)


#Calculate Current collection rate
dd["current_collection_rate"] = dd["cumulative_amount_paid"]/dd["expected_cumulative_amount_paid"]
#Calculate total amount in arrears
dd["total_arrears"] = dd["expected_cumulative_amount_paid"]-dd["cumulative_amount_paid"] 
#Calculate total Payment Progression
dd["payment_progression"] = dd["cumulative_amount_paid"]/dd["nominal_contract_value"] 
#The Expected Payment progression
dd["expected_payment_progression2"] = dd["expected_cumulative_amount_paid"]/dd["nominal_contract_value"]
#Derive name column
dd2 = dd[["contract_reference", "name"]]

#write function to calaculate loan type
def loan_type(name):
    loan_type = ""
    if 'Individual' in name:
        loan_type = "Individual Loan"
        
    elif 'Group' in name:
        loan_type = "Group Loan"
        
    elif 'Paygo' in name:
        loan_type = "Paygo Loan"
        
    elif 'Cash' in name:
        loan_type = "Cash Sale"
        
    return loan_type

dd['loan_type'] = dd['name'].apply(loan_type)

