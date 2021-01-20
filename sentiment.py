import pandas as pd


#some logistics
df = pd.read_csv('data.csv')
df = df.drop(columns=['ID','Start time', 'Email', 'Name']) #dropping irrelevant columns
df['Completion time'] = pd.to_datetime(df['Completion time'], format='%m/%d/%y %H:%M:%S') #converting to datetime
df['day_of_week'] = df['Completion time'].dt.dayofweek #weekday as int
df['hour'] = df['Completion time'].dt.hour #isolates hour as int
analysts = ['Alison', 'Derek', 'Ella', 'Emily', 'Jenny', 'Kevin', 'Meghan', 'Paggie', 'Sabine', 'Sreya']


#create list of awards, have python go through each award and add results to a new page of csv

def percent_change(new, old): #for some awards
	return (new-old) / old * 100

#print(df)

#general stats
entries_prev_year = 634
entries_current = len(df)
yoy_change = round(percent_change(entries_current, entries_prev_year),2)
print('This year, we have had over ' + str(len(df)) + ' entries! That is a ' + str(yoy_change) + ' perent change from last year!')

#slack awards


#sentiment awards
def happy_boi(): 
#highest average (tested)
	return df.groupby(['Who are you?']).mean().sort_values(by='How are you feeling?', ascending=False) 

#happy_boi()

#def most_sad(data):
	#largest difference q3 /q4

def coffee():
	#largest % change from am to pm
	final_results = []
	for name in analysts:
		am_filter = (df['Who are you?'] == name) & (df['hour'] < 12)
		pm_filter = (df['Who are you?'] == name) & (df['hour'] >= 12)
		am_df = df.loc[am_filter]
		pm_df = df.loc[pm_filter]
		am_average = am_df['How are you feeling?'].mean()
		pm_average = pm_df['How are you feeling?'].mean()
		coffee_change = percent_change(pm_average, am_average)
		final_results.append([name, coffee_change])
	final_results_sorted = sorted(final_results, key=lambda x: x[1], reverse=True)
	print(final_results_sorted)
	return pd.DataFrame(final_results_sorted, columns=['Name', 'cofee'])
#coffee()


def emotional_rollercoaster():
	#highest variance
	final_results = []
	for name in analysts:
		filtered_df = df[df['Who are you?'] == name]
		filtered_variance = filtered_df['How are you feeling?'].var()
		final_results.append([name, filtered_variance])
	final_results_sorted = sorted(final_results, key=lambda x: x[1], reverse=True)
	print(final_results_sorted)
	return pd.DataFrame(final_results_sorted, columns=['Name', 'emotional_rollercoaster'])
#emotional_rollercoaster()

def morning_bird():
	#highest percentage increase in am
	final_results = []
	for name in analysts:
		filtered_df = df[df['Who are you?'] == name]
		filtered_average = filtered_df['How are you feeling?'].mean()
		am_filter = (df['Who are you?'] == name) & (df['hour'] < 12)
		am_df = df.loc[am_filter]
		am_average = am_df['How are you feeling?'].mean()
		final_results.append([name, percent_change(am_average, filtered_average)])
	final_results_sorted = sorted(final_results, key=lambda x: x[1],reverse=True)
	print(final_results_sorted)
	return pd.DataFrame(final_results_sorted, columns=['Name', 'morning_bird'])
#morning_bird()

def weekend():
	#highest percentage increase on friday pm
	final_results = []
	for name in analysts:
		filtered_df = df[df['Who are you?'] == name]
		filtered_average = filtered_df['How are you feeling?'].mean()
		weekend_filter = (df['day_of_week'] == 4) & (df['hour'] >= 12) & (df['Who are you?'] == name)
		print(weekend_filter)
		weekend_df = df.loc[weekend_filter]
		weekend_average = weekend_df['How are you feeling?'].mean()
		final_results.append([name, percent_change(weekend_average, filtered_average)])
	final_results_sorted = sorted(final_results, key=lambda x: x[1], reverse=True)
	print(final_results_sorted)
	return pd.DataFrame(final_results_sorted, columns=['Name', 'weekend'])
#weekend()

def new_week():
	#highest percentage increase on monday am
	final_results = []
	for name in analysts:
		filtered_df = df[df['Who are you?'] == name]
		filtered_average = filtered_df['How are you feeling?'].mean()
		new_week_filter = (filtered_df['day_of_week'] == 0) & (filtered_df['hour'] <= 12)
		new_week_df = filtered_df.loc[new_week_filter]
		new_week_average = new_week_df['How are you feeling?'].mean()
		final_results.append([name, percent_change(new_week_average, filtered_average)])
	final_results_sorted = sorted(final_results, key=lambda x: x[1], reverse=True)
	print(final_results_sorted)
	return pd.DataFrame(final_results_sorted, columns=['Name', 'new_week'])
#new_week()

list_of_awards = [happy_boi, coffee, emotional_rollercoaster, morning_bird, weekend, new_week]
writer = pd.ExcelWriter('awards.xlsx')

for award in list_of_awards:
	results = award()
	results.to_excel(writer, sheet_name=str(award), index=True)
writer.save()









