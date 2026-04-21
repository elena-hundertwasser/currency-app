console.log("JS подключен");


async function convert() {
    const amount = document.getElementById('amount').value;
    const from = document.getElementById('from').value.toUpperCase();
    const to = document.getElementById('to').value.toUpperCase();

     if (!amount || amount <= 0) {
        alert("Введите сумму больше 0!");
        return;
    }

    if (from.length !== 3 || to.length !== 3) {
        alert("Валюты должны быть в формате USD, EUR и т.д.");
        return;
    }

    try {
        const response = await fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ amount: amount, from: from, to: to })
        });

        const data = await response.json();

        if (data.error) {
            document.getElementById('result').innerText = data.error;
        } else {
            document.getElementById('result').innerText =
                `${amount} ${from} = ${data.result} ${to}`;
        }

    } catch (error) {
        console.error(error);
        document.getElementById('result').innerText = "Ошибка сервера";
    }
}


async function updateRates() {
    await fetch('/update_rates', { method: 'POST' });
    getTime();
}


async function getTime() {
    const res = await fetch('/last_update');
    const data = await res.json();

    document.getElementById('time').innerText =
        "Последнее обновление: " + data.last_update;
}


getTime();
