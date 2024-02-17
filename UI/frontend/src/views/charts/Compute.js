
export const computePlayerdata = (data) => {
    
    let dataArray = [];
    data.forEach(element => {
        let obj = JSON.parse(element.data)
        dataArray = dataArray.concat(obj)
    });

    let spliceArray = [];
    for (let i = 0; i < dataArray.length; i++) {
        let date = dataArray[i][0];
        for (let j = 0; j < dataArray[i].length; j++) {
            if (date === dataArray[j][0] && j !== i) {
                dataArray[i][1] += dataArray[j][1]
                spliceArray.push(j)
                i++;
            }
        }
    }
    for (let i = 0; i < spliceArray.length; i++) {
        dataArray.splice(spliceArray[i] - i, 1)
    }


    let new_data = dataArray.map(([a, b]) => [new Date(a), b]);
    return new_data
}

const getAvarage=(array)=>{
     
     let avg=array.reduce((sum,value)=>{
        return sum+value
     },0) / array.length;
     return avg
}

export const computeTotalData = (data) => {
    let dataArray = [];
    data.forEach(element => {
        let obj = JSON.parse(element.data)
        dataArray = dataArray.concat(obj)
    });

    
    // to test avg function dataArray.push(['12/05/1999',108.75])
    let spliceArray = [];
    for (let i = 0; i < dataArray.length; i++) {
        let date = dataArray[i][0];
        for (let j = 0; j < dataArray[i].length; j++) {
            if (date === dataArray[j][0] && j !== i) {
                dataArray[i][1] += dataArray[j][1]
                spliceArray.push(j)
                i++;
            }
        }
    }
    for (let i = 0; i < spliceArray.length; i++) {
        dataArray.splice(spliceArray[i] - i, 1)
    }
    let fatigues = {}

    
    //creates {date:[score1,score2]}
    dataArray.forEach((element) => {
        let date = element[0]
        let score = element[1]
        if (date in fatigues) {
            fatigues[date].push(score)
        }
        else {
            fatigues[date]=[score]
        }
    })

    Object.keys(fatigues).forEach((element)=>{
        fatigues[element]= getAvarage(fatigues[element])
    })


    let new_data = Object.keys(fatigues).map((key) => [new Date(key), fatigues[key]]);
    return new_data

}


