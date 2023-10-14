var tg = window.Telegram.WebApp;

tg.expand();
tg.MainButton.textColor = "#FFF";
tg.MainButton.color = "#9b2f12";

let item = '';

let products = [
    ['Беккен', 40],
    ['Сосиска в тесте', 50],
    ['Очпочмак', 57],
    ['Круассан', 56],
    ['Пицца', 53],
]

str = "";

for(let i = 0; i < products.length; i++)
{
    str += "<div class=\"item btn\">\n" +
        "                <img src=\"img"+(i+1)+".png\" alt=\"\" class=\"img\">\n" +
        "                <br />\n" +
        "                <span class='name'>"+products[i][0]+" | "+products[i][1]+" руб.</span>\n" +
        "                <br />\n" +
        "                <button class=\"sub-btn\" style=\"display: none\">-</button>\n" +
        "                <span style=\"display: none;\" class=\"value\">0</span>\n" +
        "                <button class=\"add-btn\">Добавить</button>\n" +
        "            </div>"
}
document.getElementById('inner').innerHTML = str;

let product = [];
product.length = products.length;
for(let j = 0; j < product.length; j++)
{
    product[j] = 0;
}

let addBtn = document.getElementsByClassName('add-btn');
let subBtn = document.getElementsByClassName('sub-btn');
let value = document.getElementsByClassName('value');
let btn = document.getElementsByClassName('btn');
for(let i = 0; i < addBtn.length; i++)
{
    addBtn[i].onclick = function (){
        product[i]++;
        addBtn[i].innerHTML = "+";
        subBtn[i].style.display = "";
        value[i].style.display = "";
        value[i].innerHTML = "&nbsp;" + product[i] + " ";
        let sum = 0;
        for(let j = 0; j < product.length; j++)
        {
            sum += product[j];
        }
        if(!sum && tg.MainButton.isVisible) {
            tg.MainButton.hide();
        } else {
            let val = 0;
            for (let j = 0; j < product.length; j++) val += product[j]*products[j][1];
            tg.MainButton.setText("Выбрано товаров: " + sum + " | Итого: " + val + " руб.");
            console.log("Итого:" + val + " руб.");
            if(!tg.MainButton.isVisible) tg.MainButton.show();
        }
    };
    subBtn[i].onclick = function () {
        product[i]--;
        value[i].innerHTML = "&nbsp;" + product[i] + " ";
        if (!product[i]) {
            addBtn[i].innerHTML = "Добавить";
            subBtn[i].style.display = "none";
            value[i].style.display = "none";
        }
        let sum = 0;
        for(let j = 0; j < product.length; j++)
        {
            sum += product[j];
        }
        if(!sum && tg.MainButton.isVisible) {
            tg.MainButton.hide();
        } else {
            let val = 0;
            for (let j = 0; j < product.length; j++) val += product[j]*products[j][1];
            tg.MainButton.setText("Выбрано товаров: " + sum + " | Итого: " + val + " руб.");
            let str = "";
            for(let i = 0; i < product.length; i++) str += product[i] + " ";
            console.log(str);
            if(!tg.MainButton.isVisible) tg.MainButton.show();
        }
    };
}
Telegram.WebApp.onEvent('mainButtonClicked', function(){
    let val = 0;
    for (let j = 0; j < product.length; j++) val += product[j]*products[j][1];
    let str = prompt("Введите номер кабинета:");
    for(let i = 0; i < product.length; i++) str += " " + product[i];
    str += " " + val
    console.log(str);
    tg.sendData(str);
    //при клике на основную кнопку отправляем данные в строковом виде
});


let usercard = document.getElementById('usercard');

let p = document.createElement('p');
p.innerText = `${tg.initDataUnsafe.user.first_name}` +
    `${tg.initDataUnsafe.user.last_name}`
usercard.appendChild(p);