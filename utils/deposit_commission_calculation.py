def calculate_balances_for_deposit(sent_amount, merchant_balance, agent_balance, merchant_commission,
                                    agent_commission):

    # Calculate the merchant balance after withdrawal
    merchant_commission_amount_n_balance = sent_amount - (sent_amount * merchant_commission) / 100
    merchant_balance_after = merchant_balance + merchant_commission_amount_n_balance

    # Calculate the agent balance after commission
    agent_commission_amount_n_balance = (sent_amount * agent_commission) / 100 + sent_amount
    agent_balance_after = agent_balance - agent_commission_amount_n_balance

    return merchant_balance_after, agent_balance_after, merchant_commission_amount_n_balance, agent_commission_amount_n_balance

