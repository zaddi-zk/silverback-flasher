const amountButtons = document.querySelectorAll('.amount-btn');
const paymentButtons = document.querySelectorAll('.payment-btn');
const customAmount = document.getElementById('customAmount');
const selectedCurrency = document.getElementById('selectedCurrency');
const selectedAddress = document.getElementById('selectedAddress');
const startBridge = document.getElementById('startBridge');
const paymentCard = document.getElementById('paymentCard');
const paymentIdField = document.getElementById('paymentId');
const paymentAmountField = document.getElementById('paymentAmount');
const paymentCurrencyField = document.getElementById('paymentCurrency');
const expectedReceiveField = document.getElementById('expectedReceive');
const estimatedFeeField = document.getElementById('estimatedFee');
const paymentNetworkField = document.getElementById('paymentNetwork');
const paymentAddressField = document.getElementById('paymentAddress');
const confirmPayment = document.getElementById('confirmPayment');
const txHashInput = document.getElementById('txHash');

let selectedAmount = 100;
let selectedMethod = 'BTC';
let orderData = null;

function setActiveAmount(button) {
    amountButtons.forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
    selectedAmount = Number(button.dataset.value);
    customAmount.value = '';
}

function setActivePayment(button) {
    paymentButtons.forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
    selectedMethod = button.dataset.currency;
    selectedCurrency.innerText = selectedMethod;
    selectedAddress.innerText = button.dataset.address;
}

amountButtons.forEach(button => {
    button.addEventListener('click', () => setActiveAmount(button));
});

paymentButtons.forEach(button => {
    button.addEventListener('click', () => setActivePayment(button));
});

customAmount.addEventListener('input', () => {
    const value = Number(customAmount.value);
    if (value >= 20) {
        selectedAmount = value;
        amountButtons.forEach(btn => btn.classList.remove('active'));
    }
});

txHashInput.addEventListener('input', () => {
    const value = txHashInput.value.trim();
    const valid = value.startsWith('0x') && value.length >= 20;
    confirmPayment.disabled = !valid;
    confirmPayment.classList.toggle('disabled', !valid);
});

startBridge.addEventListener('click', async () => {
    const amount = selectedAmount;
    const currency = selectedMethod;
    startBridge.innerText = 'Generating...';
    startBridge.disabled = true;

    try {
        const response = await fetch('/initiate-payment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount, currency })
        });
        const data = await response.json();
        startBridge.innerText = 'Generate Payment';
        startBridge.disabled = false;

        if (data.success) {
            paymentCard.classList.remove('hidden');
            orderData = data;
            paymentIdField.innerText = data.payment_id;
            paymentAmountField.innerText = `$${data.amount_usd.toFixed(2)}`;
            paymentCurrencyField.innerText = data.currency;
            expectedReceiveField.innerText = data.receive_amount;
            estimatedFeeField.innerText = data.expected_fee;
            paymentNetworkField.innerText = data.network;
            paymentAddressField.innerText = data.wallet_address;
            confirmPayment.disabled = true;
            confirmPayment.classList.add('disabled');
        }
    } catch (error) {
        console.error(error);
        startBridge.innerText = 'Generate Payment';
        startBridge.disabled = false;
    }
});

confirmPayment.addEventListener('click', async () => {
    if (!orderData) return;
    const txHash = txHashInput.value.trim();
    confirmPayment.innerText = 'Submitting...';
    confirmPayment.disabled = true;

    try {
        const response = await fetch('/confirm-payment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ payment_id: orderData.payment_id, tx_hash: txHash })
        });
        const data = await response.json();
        if (data.success) {
            window.location.href = `/processing?payment_id=${orderData.payment_id}`;
        } else {
            confirmPayment.innerText = 'I Have Sent Payment';
            confirmPayment.disabled = false;
        }
    } catch (error) {
        console.error(error);
        confirmPayment.innerText = 'I Have Sent Payment';
        confirmPayment.disabled = false;
    }
});

window.addEventListener('DOMContentLoaded', () => {
    const firstPaymentBtn = document.querySelector('.payment-btn');
    if (firstPaymentBtn) {
        firstPaymentBtn.dataset.address = document.getElementById('selectedAddress').innerText;
        firstPaymentBtn.click();
    }
});
