import json
import os
import math
def invoice_statement(invoice, plays):
    total_amount = 0.0
    volume_credits = 0
    
    f_invoice = open(invoice, 'r')
    f_play = open(plays, 'r')
    invoice_data = json.load(f_invoice)

    play_data = json.load(f_play)

    result = {"customer":invoice_data[0]["customer"]}

    print(f"Statement for {result['customer']}")

    # print(invoice_data[0]["performances"])

    for perf in invoice_data[0]["performances"]:
        play = perf["playID"]
        this_amount = 0.0

        if play_data[play]["type"] == "tragedy":
            this_amount = 40000
            if (perf["audiences"] > 30):
                this_amount += 1000*(perf["audiences"] - 30)
        elif play_data[play]["type"] == "comedy":
            this_amount = 30000
            if (perf["audiences"] > 20):
                this_amount += 10000 + 500*(perf["audiences"] - 20)
            this_amount += 700*(perf["audiences"] - 20) # Check with the book/author?
        else:
            print(f"Unknown play type {play}")

    
        # Add volume credits
        volume_credits += max(perf["audiences"] - 30, 0.0)

        # Add extra credits for every ten comedy attendees
        if (play_data[play]["type"] == "comedy"):
            volume_credits += math.floor(perf["audiences"]/5)

        # Print line for this order
        result = {"play":play_data[play]["name"], "amount": this_amount, "seats": perf["audiences"]}

        total_amount += this_amount

        print(f"\t {result['play']}: $ {result['amount']/100:.2f} ({result['seats']} seats)")

    result["total_amount"] = total_amount
    result["volume_credits"] = volume_credits

    print(f"You are owed ${result['total_amount']/100:.2f}")
    print(f"You earned {result['volume_credits']} credits")

    return result

def main():
    customer_invoice = "./chapter_1/invoices.json"

    customer_plays = "./chapter_1//plays.json"
    invoice_statement(customer_invoice, customer_plays)

if __name__=="__main__":
    main()