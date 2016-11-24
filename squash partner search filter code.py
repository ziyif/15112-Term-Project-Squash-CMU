
requirements={
    'gender':'F'
    'min_level': 1.0,
    'max_level': 2.0,
    'timesPreferred':{0,1,10}
    'frequency': 3,
    'importance': {
        'gender': 5,
        'time': 2
    }
}

users={
    'Flora':{
        'name': 'flora'
        'gender':'F'
        'min_level': 1.0,
        'max_level': 2.0,
        'timesPreferred':{0,1,10}
        'frequency': 3,
    }
    "Alpha":
    "Beta":
}

# requirements['im']['ge']
# [['F',(1.0,2.0),{0,1,10},3],[5,6,7,8]]

    
def filter(requirements,users):
    result=dict()
    for key in users:
        # list 
        userInfo=d[key]
        
        importance=requirements['importance']  # dictionary

        totalImportanceScore=0

        for key in importance:
            totalImportanceScore+=importance[key]


        # gender
        if userInfo['gender']==requirements['gender']:
            weightA=importance['gender']/totalImportanceScore
            scoreA= 1*weightA
        else:
            scoreA=0

        # level
        userLevel=userInfo['level']
        min_level=requirements['min_level']
        max_level=requirements['max_level']
        weightB=importance['level']/totalImportanceScore
        if min_level<=userLevel<=max_level:
            scoreB= 1* weightB
        elif userLevel<min_level:
            scoreB=1*(1/3)**(min_level-userLevel)*weightB


        #timesPreferred
        requirementTime=requirements['timesPreferred']

        frequency=requirements['frequency']

        userTime=userInfo['timesPreferred']

        commonTimes=requirementTime.union(userTime)
        numOfCommonBlocks=len(commonTimes)
        weightC=importance['timesPreferred']/totalImportanceScore
        if numOfCommonBlocks>=frequency:
            scoreC=1*weightC
        else:
            scoreC=numOfCommonBlocks/frequency*weightC


        # frequency
        weightD=importance['frequency']/totalImportanceScore
        userFrequency=userInfo['frequency']
        scoreD=min(userFrequency,frequency)/max(userFrequency,frequency)*weightD

        totalScore=scoreA+scoreB+scoreC+scoreD

        if totalScore> 0.7:
            result.append({key:d[key],'score':totalScore})

        return result


