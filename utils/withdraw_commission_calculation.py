def calculate_balances_for_withdraw(requested_amount, merchant_balance, agent_balance, merchant_commission,
                                    agent_commission):
    # Calculate the merchant balance after withdrawal
    merchant_commission_amount_n_balance = (requested_amount * merchant_commission) / 100 + requested_amount
    merchant_balance_after = merchant_balance - merchant_commission_amount_n_balance

    # Calculate the agent balance after commission
    agent_commission_amount_n_balance = (requested_amount * agent_commission) / 100 + requested_amount
    agent_balance_after = agent_balance - agent_commission_amount_n_balance

    return merchant_balance_after, agent_balance_after, merchant_commission_amount_n_balance, agent_commission_amount_n_balance
