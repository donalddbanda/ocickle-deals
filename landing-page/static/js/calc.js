function calcEscrowCost(e) {
    const submitBtn = document.querySelector(`#submitEcsrowAmount`)

    submitBtn.addEventListener("click", calculateEscrowCost)

}

function calculateEscrowCost(e) {
    const amount = Number(document.querySelector('#amount').innerHTML);

    if (amount <= 20000) {
        const escrowFee = 1000;
        const escrowCost = escrowFee; // Assuming escrowCost is just the fee here? Or fee + amount? 
        // Based on other blocks, escrowCost seems to be the total charge. 
        // But let's look at the other blocks:
        // const escrowCost = escrowFee + paymentProcessingFee
        // Here we probably don't have paymentProcessingFee or it's 0. 

        return { escrowFee, escrowCost };
    }

    else if (amount >= 250000) {
        const paymentProcessingFee = (amount * 6) / 100
        const escrowFee = 15000 + paymentProcessingFee
        const escrowCost = escrowFee + paymentProcessingFee

        return { escrowFee, paymentProcessingFee, escrowCost };
    }

    else {
        const paymentProcessingFee = (amount * 6) / 100
        const escrowFee = (amount * 2) / 100;
        const escrowCost = escrowFee + paymentProcessingFee

        return { escrowFee, escrowCost, paymentProcessingFee };
    }

    // document.querySelector('')
}

export { calcEscrowCost }