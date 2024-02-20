## Context

The purpose of this exercise is to assess how you would go about building a clasification system using a  [Kaggle heart disease](https://www.kaggle.com/code/kaanboke/beginner-friendly-catboost-with-optuna/notebook) . It is meant to give you a taste of a type of problem that you would work on as part of our team, and to give us an idea of how you would approach tackling it.

## Problem statement

Your goal is to use the data from the [Kaggle heart disease](https://www.kaggle.com/code/kaanboke/beginner-friendly-catboost-with-optuna/notebook) to develop a clasification system that predicts the user will have heart disease.

Conceptually, for a given the next ferature.

```python
1. Age: age of the patient [years]
2. Sex: sex of the patient [M: Male, F: Female]
3. ChestPainType: chest pain type [TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic]
4. RestingBP: resting blood pressure [mm Hg]
5. Cholesterol: serum cholesterol [mm/dl]
6. FastingBS: fasting blood sugar [1: if FastingBS > 120 mg/dl, 0: otherwise]
7. RestingECG: resting electrocardiogram results [Normal: Normal, ST: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV), LVH: showing probable or definite left ventricular hypertrophy by Estes' criteria]
8. MaxHR: maximum heart rate achieved [Numeric value between 60 and 202]
9. ExerciseAngina: exercise-induced angina [Y: Yes, N: No]
10. Oldpeak: oldpeak = ST [Numeric value measured in depression]
11. ST_Slope: the slope of the peak exercise ST segment [Up: upsloping, Flat: flat, Down: downsloping]
```
The system should return if the user will have a heart disease.

## Instructions

> These instructions are not overly prescriptive by design: we want to provide you enough details so you know what we expect, while also giving you freedom to choose how you tackle the problem.

1. Visit the [Kaggle heart disease](https://www.kaggle.com/code/kaanboke/beginner-friendly-catboost-with-optuna/notebook) page on Kaggle. Read the details of the data and download it. _If you don’t have a Kaggle account, you will need to create one in order to download the data._
2. You must use Python as the programming language to develop your solution in notebooks and/or Python modules, but you are free to use any open source libraries and tools.
3. Fork the repository to develop your solution.
4. Solving this problem in production, at scale, is difficult. The intention behind this take home exercise is to see how you would approach building a quick solution to it (while learning new topics you may not be too familiar with). We do not expect you to deliver production-quality code, but try to use best-practices when implementing your solution. _Tip: if you are running low on time, aim to have a suboptimal, but working solution.
  
**Submitting your solution**

   - Once you’re happy with your solution, submit it by raising a pull request in this repo, adding `joenvihe` as a reviewer. Please include all the notebooks and/or modules you end up writing, and include instructions to run your solution.

## What we will evaluate

- Your overall approach to tackling the problem.
- If you can submit a working solution, or how close you get to it.
- How well you structure your solution.
- Maintainability of your solution.
- Best practices
test2222
