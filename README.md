This code is designed to render the angular momentum envelope for various setups of CMG clusters.
To use it:

1. Firstly, you need to adjust the settings in the "Settings.json" file.
2. There are two choices for the "Cluster Combination", "adj" or "pyr." Meaning the "Adjacent Pair(2x)" or "Pyramid Cluster(4x)" of the CMG. The adjacent pair combination of CMG is #1 and #4 CMG in "A Control Moment Gyro (CMG) Based Attitude Control System (ACS) for Agile Small Satellites": https://openresearch.surrey.ac.uk/esploro/outputs/doctoral/A-Control-Moment-Gyro-CMG-Based/99516248502346
3. There are two choices for the "Cluster Style", "conv" or "hans." This means the "Conventional" or "Hanspeter" way of defining skew angle. (beta)
4. There are two choices for the "Speed Type", "CS" or "VS." Meaning "Constant-Speed" or "Variable-Speed."
5. Then run the file od "Angular_Momumtum_Envelop.py". You should get the following figures.
6. Settings for the example figures:

```json
{ 
    "Skew Angle":53.13,
    "Max. Angular Momemtum per CMG":100,
    "Delta H for Simulation":0.1,
    "Delta Theta for Simulation":5,
    "Cluster Combination":"adj",
    "Cluster Style":"conv",
    "Speed Type":"CS"
}
```

![Example_Full](https://github.com/user-attachments/assets/23e4b5e2-f28b-42b2-b17d-768f2f851fd4)

![Example_X](https://github.com/user-attachments/assets/5e7c35ef-f427-402d-a72a-1991a68cc0c9)

![Example_Y](https://github.com/user-attachments/assets/2baf8e8b-9c3f-46a7-9302-0c1b2f30bfdd)

![Example_Z](https://github.com/user-attachments/assets/1c01d350-1428-430c-b537-c73d0a85ab73)

7. Prints in the terminal:

```
Processing it1 (adj): 100%|████████████████████████████████████████████████████████████████████████| 72/72 [00:00<00:00, 1629.97it/s] 

X-axis Size for the Angular Momentum Envelope: 1.6000e+02
Y-axis Size for the Angular Momentum Envelope: 1.6000e+02
Z-axis Size for the Angular Momentum Envelope: 1.6000e+02

Radius of the inscribed sphere: 1.1312e+02
```
