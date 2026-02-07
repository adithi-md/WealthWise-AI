def get_response(user_input, user_profile):
    text = user_input.lower()

    if "sip" in text:
        return (
            "A SIP (Systematic Investment Plan) means investing a small fixed amount "
            "every month in a mutual fund. It helps build wealth slowly and reduces "
            "risk by spreading investments over time."
        )

    elif "mutual fund" in text:
        return (
            "A mutual fund pools money from many investors and invests it in stocks, "
            "bonds, or other assets, managed by professionals."
        )

    elif "stock" in text:
        return (
            "Stocks represent ownership in a company. When the company grows, the "
            "value of your shares can increase."
        )

    else:
        return "Please ask questions related to investments like SIP, mutual funds, or stocks."
