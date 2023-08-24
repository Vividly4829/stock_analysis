import json
# import a json file and read it
data = None
with open('results-Survey.json') as f:
    data = json.load(f)
    # print(data)

values = []
for result in data:
    # print(result['value'])
    values.append(result['value'])

# convert values to a dict where we count for each value how often it occurs
counts = {}
for value in values:
    if value in counts:
        counts[value] += 1
    else:
        counts[value] = 1


# plot the values
import matplotlib.pyplot as plt
# at a legend to the plot 'minutes saved per hour of work'
# plot counts dict
# Make the background black
plt.style.use('dark_background')

plt.bar(counts.keys(), counts.values())
# add an x-axis label 'minutes saved per hour of work'
plt.xlabel('minutes saved per hour of work')
# add a y-axis label 'number of people'
plt.ylabel('number of people reporting this number')
# Add a title
plt.title('How much time do you save per hour of work with faster loading times?')
# show the average value on the plot
plt.axvline(x=sum(values)/len(values), color='red', label='average')
# show the median value on the plot
plt.axvline(x=sorted(values)[len(values)//2], color='yellow', label='median')
# add a legend
plt.legend()
# Add a note to the bottom of the plot
plt.figtext(0.5, 0.01, '54 users reported that on average 5 min per hour or 38,5 min per day can be saved with near instant loading', ha='center', fontsize=6, color='white')
# make the plot dark themed
plt.style.use('dark_background')



plt.show()
