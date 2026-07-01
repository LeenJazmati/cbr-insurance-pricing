# CBR Insurance Pricing System

A Case-Based Reasoning (CBR) expert system that estimates health insurance prices by comparing new cases to previously stored cases and reusing the price of the most similar match.

## Overview

Traditional insurance pricing relies on statistical models or machine learning approaches that often require large amounts of training data and can be difficult to interpret. This project explores a simpler, more transparent alternative: Case-Based Reasoning.

Instead of learning patterns from data through training, the system reasons by analogy — retrieving the closest historical case to a new one, and using its known price as the estimate. Every prediction is fully traceable back to the case that produced it.

## How It Works

The system follows the four core stages of the CBR cycle:

1. **Retrieve** — When a new case is entered, the system checks whether it already exists in the database. If not, it calculates the distance between the new case and every stored case, then retrieves the closest match.
2. **Reuse** — The insurance price of the closest matching case is used as the estimate for the new case.
3. **Revise** — The estimated result is reviewed for consistency before being finalized.
4. **Retain** — The new case, along with its estimated price, is saved back into the dataset, allowing the knowledge base to grow and improve over time.

### Distance Function

Similarity between cases is calculated using **Manhattan Distance** across six attributes: Age, Sex, BMI, Children, Smoker status, and Region.

```
d[i] = |x_new[i] - x_stored[i]|
D_total = Σ d[i]
```

The case with the lowest total distance is considered the nearest match.

## Dataset

- **Source:** [Kaggle — Medical Cost Personal Datasets](https://www.kaggle.com/datasets/mirichoi0218/insurance)
- **Records:** ~1,338
- **Attributes:** Age, Sex, BMI, Children, Smoker, Region, Charges (target)

Categorical variables were encoded numerically (e.g., Sex: male=0, female=1; Smoker: no=0, yes=1; Region: southwest=0, southeast=1, northwest=2, northeast=3) to allow distance-based comparison.

> **Note:** The dataset file (`insurance_original.csv`) is included in this repository. Make sure it stays in the same folder as the code — the script reads it using a relative path.

## Interface

A graphical interface built with **CustomTkinter** allows users to input a new case (numerical fields for Age/BMI/Children, dropdown menus for categorical values) and instantly view the closest matching case along with the predicted price, displayed in a dedicated highlighted price card.

## Results

The system was tested on five diverse cases. Across all tests, **smoking status consistently emerged as the single strongest driver of predicted price**, followed by age and BMI — closely matching real-world insurance pricing patterns. For example, two cases with nearly identical age and BMI but different smoking status showed a dramatic difference in estimated cost, confirming the system's logic aligns with real insurance risk factors.

## Tech Stack

- Python
- Pandas / NumPy
- CustomTkinter (GUI)

To run the interface, install the required package first:

```
pip install customtkinter
```

## References

- Kaggle. (2024). *Medical Cost Personal Datasets*. [Link](https://www.kaggle.com/datasets/mirichoi0218/insurance)
- Aamodt, A., & Plaza, E. (1994). *Case-Based Reasoning: Foundational Issues, Methodological Variations, and System Approaches*. AI Communications, 7(1), 39-59.
- Watson, I. (1999). *Case-Based Reasoning is a Methodology not a Technology*. Knowledge-Based Systems, 12(5-6), 303-308.
- Kolodner, J. (1993). *Case-Based Reasoning*. Morgan Kaufmann Publishers.
- Richter, M. M., & Weber, R. O. (2013). *Case-Based Reasoning: A Textbook*. Springer.

## Author

**Leen Jazmati**
Aleppo University — Faculty of Informatics Engineering, Artificial Intelligence Department

