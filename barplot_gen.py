import matplotlib.pyplot as plt
import matplotlib

def generate_barplot(values,day):
    matplotlib.use('agg')
    try:
        keys=[]
        for num in range(1,len(values)+1):
            keys.append('Gen'+str(num))
        values=values
        fig = plt.figure(figsize = (6,5))
        plt.bar(keys,values,color='#fa4a04',width=0.3)
        for i, value in enumerate(values):
            plt.text(i, value + 0.3, str(value), ha='center', va='bottom')
        plt.xlabel("Generations based on different mutation rate")
        plt.ylabel("Total calories Burnt")
        plt.title("Best Exercise plan")
        name='static/images/barplot'+str(day)+'.png'
        plt.savefig(name)
        plt.close()
    except:
        pass

if __name__=='__main__':
    generate_barplot({690, 630, 495},2)