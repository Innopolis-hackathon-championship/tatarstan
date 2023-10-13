var tg = window.Telegram.WebApp;

tg.expand();
tg.MainButton.textColor = "#FFF";
tg.MainButton.color = "#703f05";

let item = '';

let product = [];
product.length = 6;
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
        value[i].innerHTML = product[i];
        let sum = 0;
        for(let j = 0; j < product.length; j++)
        {
            sum += product[j];
        }
        if(!sum && tg.MainButton.isVisible) {
            tg.MainButton.hide();
        } else {
            tg.MainButton.setText("Выбрано товаров: " + sum);
            console.log("Выбрано товаров: " + sum);
            if(!tg.MainButton.isVisible) tg.MainButton.show();
        }
    };
    subBtn[i].onclick = function () {
        product[i]--;
        if (!product[i]) {
            addBtn[i].innerHTML = "Купить";
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
            tg.MainButton.setText("Выбрано товаров: " + sum);
            console.log("Выбрано товаров: " + sum);
            if(!tg.MainButton.isVisible) tg.MainButton.show();
        }
    };
}

Telegram.WebApp.onEvent("mainButtonClicked", function () {
    Telegram.sendData(item);
});

let usercard = document.getElementById('usercard');

let p = document.createElement('p');
p.innerText = `${tg.initDataUnsafe.first_name}`
    `${tg.initDataUnsafe.first_name}`
usercard.appendChild(p);