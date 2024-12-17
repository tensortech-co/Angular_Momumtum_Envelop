This code is designed to render the angular momentum envelope for various setups of CMG clusters.
To use it:

1. Firstly, you need to adjust the settings in the "Settings.json" file.
2. There are four choices for the "Cluster Combination", "adj", "pyr", "3RW", or "4RW." Meaning the "Adjacent Pair(2x)", "Pyramid Cluster(4x)" of the CMG, "Reaction Wheels(3x) placing in orthogonal configuration", or "Reaction Wheels(4x) placing in Pyramid Cluster". The adjacent pair combination of CMG is #1 and #4 CMG in "A Control Moment Gyro (CMG) Based Attitude Control System (ACS) for Agile Small Satellites": https://openresearch.surrey.ac.uk/esploro/outputs/doctoral/A-Control-Moment-Gyro-CMG-Based/99516248502346
3. There are two choices for the "Cluster Style", "conv" or "hans." This means the "Conventional" or "Hanspeter" way of defining skew angle. (beta)
4. There are two choices for the "Speed Type", "CS" or "VS." Meaning "Constant-Speed" or "Variable-Speed." For 3RW or 4RW, this setting won't impact the calculations.
5. Then run the file "Angular_Momumtum_Envelop.py". You should get the following figures.
6. Settings for the example figures:

```json
{ 
    "Skew Angle":53.13,
    "Max. Angular Momemtum per CMG":1,
    "No. of Delta H Segment":2,
    "No. of Delta Theta Segment":20,
    "Cluster Combination":"pyr",
    "Cluster Style":"conv",
    "Speed Type":"VS",
    "Wrap Shape N_theta":9,
    "Wrap Shape N_phi":15
}
```

![Z](https://github.com/user-attachments/assets/d9f6d943-40d2-4ed3-8d14-30f1adca0694)
![Y](https://github.com/user-attachments/assets/ee64c501-2672-4e90-82e2-3754bd1fc04e)
![X](https://github.com/user-attachments/assets/25eeddba-5a35-4822-8a1c-5c39507794a7)
![Full](https://github.com/user-attachments/assets/326898f4-99d5-4968-828b-bb1c00affe80)


7. Prints in the terminal:

```
X-axis Size for the Angular Momentum Envelope: 3.1839e+00
Y-axis Size for the Angular Momentum Envelope: 3.1839e+00
Z-axis Size for the Angular Momentum Envelope: 3.1878e+00

Radius of the inscribed sphere: 2.8841e+00
```
