const makeWithdraw = 
    (balance) => (
      (copyBalance) => {

        let balance = copyBalance; // This variable is private

        const doBadThings = () => {
          console.log("I will do bad things with your money");
        };

        doBadThings();

        return {
            withdraw(amount) {
                if (balance >= amount) {
                    balance -= amount;
                    return balance;
                }
                return "Insufficient money";
            },
            withdrawb(amount) {
                if (balance >= amount) {
                    balance -= amount;
                    return balance;
                }
                return "Insufficient money";                    
            }
        };

      } 
    ) (balance);

exports.makeWithdraw=makeWithdraw