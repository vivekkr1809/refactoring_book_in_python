import json
import sys
import math
def invoice_statement(invoice, plays):
    total_amount = 0.0
    volume_credits = 0

    f_invoice = open(invoice, 'r')
    f_play = open(plays, 'r')

    invoice_data = json.load(f_invoice)[0]

    play_data = json.load(f_play)

    result = f"Statement for {invoice_data['customer']} \n"

    for perf in invoice_data["performances"]:
        play = play_data[perf["playID"]]
        this_amount = 0.0

        if play["type"] == "tragedy":
            this_amount = 40000
            if (perf["audiences"] > 30):
                this_amount += 1000*(perf["audiences"] - 30)
        elif play["type"] == "comedy":
            this_amount = 30000
            if (perf["audiences"] > 20):
                this_amount += 10000 + 500*(perf["audiences"] - 20)
            this_amount += 300*perf["audiences"]
        else:
            print(f"Unknown play type {play['type']}")

    
        # Add volume credits
        volume_credits += max(perf["audiences"] - 30, 0.0)

        # Add extra credits for every ten comedy attendees
        if (play["type"] == "comedy"):
            volume_credits += math.floor(perf["audiences"]/5)

        # Print line for this order
        result += f" {play['name']}: ${this_amount/100:.2f} ({perf['audiences']} seats) \n"

        total_amount += this_amount
    
    result += f"Amount owed is ${total_amount/100:.2f} \n"
    result += f"You earned {volume_credits} credits \n"

    return result

def main():
    customer_invoice = "./chapter_1/invoices.json"

    customer_plays = "./chapter_1//plays.json"
    print(invoice_statement(customer_invoice, customer_plays))

if __name__=="__main__":
    main()