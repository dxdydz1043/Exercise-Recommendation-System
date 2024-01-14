import matplotlib.pyplot as plt
import matplotlib

def generate_piechart(values,day):
    matplotlib.use('agg')
    try:
        values=sorted(values,key=lambda x:x[0])
        vals=[]
        labels=[]
        for val in values:
            vals.append(val[0])
            labels.append(val[1])
        explode = [0, 0, 0, 0, 0.2]

        def return_value(vals):
            return str(vals.pop(0)) + ' cals'
        
        fig = plt.figure(figsize = (6, 5))
        plt.pie(vals, labels = labels,
                autopct=lambda val : return_value(vals), 
                explode=explode,  
            shadow = True)
        plt.title('Excercise and Calories')
        name='static/images/pieplot'+str(day)+'.png'
        plt.savefig(name)
        plt.close()
    except:
        pass


if __name__ == '__main__':
    generate_piechart([[180, 'Incline Push-ups'], [120, 'Butt Bridge'], [240, 'Knee to Chest Stretch'], [180, 'Leg Barbell Curl'], [60, 'Rhomboid Pulls']],2)
