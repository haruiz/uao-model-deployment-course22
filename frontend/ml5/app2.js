async function getLastNASAPicture(){
    const url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY";
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

async function closestAsteroidsToEarth(){
    const url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key=DEMO_KEY";
    const response = await fetch(url);
    const data = await response.json();
    return data;
}


function getNASAData(){
    // return new Promise(async(resolve, reject) => {
    //     try {
    //         const data = await getLastNASAPicture();
    //         const data2 = await closestAsteroidsToEarth();
    //         resolve({data, data2});
    //     } catch (error) {
    //         reject(error);
    //     }
   
    // });
    return Promise.all([getLastNASAPicture(), closestAsteroidsToEarth()]);
}



document.addEventListener("DOMContentLoaded", async function() {
    const result = await getNASAData();
    console.log(result);
});
