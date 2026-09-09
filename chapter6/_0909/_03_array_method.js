let names = ["염", "예", "찬"];

names.forEach((n)=>{

})

let numbers = [1,2,3,4,5]
let double_numbers;
// [  2, 4, 6, 8, 10  ]
double_numbers = numbers.map( (n)=>{ return n * 2; } )

let ages = [15, 22, 13, 29, 19, 35];
// [ 22, 29 , 19, 35  ] 
let filtered_ages ;
filtered_ages = ages.filter(  (age)=>{ return age >= 19; }  )

let ages2 = [15, 22, 13, 29, 19, 35];
let target;
target = ages2.find(  (age) => { return age >= 19; }  )

let numbers2 = [10,20,30,40,50];
// 1 - result : 0   cur : 10   -> 10
// 2 - result : 10  cur : 20   -> 30
// 3 - result : 30  cur : 30   -> 60
// 4 - result : 60  cur : 40   -> 100
// 5 - result : 100 cur : 50   -> 150
let sum;
sum = numbers2.reduce(  (result, cur) => {  return result + cur; }  )