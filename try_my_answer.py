import pandas as pd
from task_Jan_Zdyb import add_virtual_column

def main()->None:
    df=pd.DataFrame(
        {
            "quality":[86,22,7],
            "price":[90,41,62],
        }
    )
    print(f"Original DataFrame:\n{df}")

    result_add=add_virtual_column(
        df,
        "quality+price",
        "sum"
    )
    print(f"\nAddition DataFrame:\n{result_add}")

    result_sub=add_virtual_column(
            df,
            "quality-price",
            "sub"
        )
    print(f"\nSubstraction DataFrame:\n{result_sub}")

    result_mul=add_virtual_column(
            df,
            "quality*price",
            "mul"
        )
    print(f"\nMultiplication DataFrame:\n{result_mul}")

    result_super=add_virtual_column(
            df,
            "quality*(price-price)",
            "mul"
        )
    print(f"\nSuper DataFrame:\n{result_super}")

    result_inv=add_virtual_column(
                df,
                "quality/price",
                "inv"
            )
    print(f"\nInvalid DataFrame:\n{result_inv}")

if __name__=="__main__":
    main()