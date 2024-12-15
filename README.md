This code is designed for rendering the angular momentum envelop for various setups of CMG clusters.
To use it:

1. firstly, you need to adjust settings in the "Settings.json" file.
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

![Example_Full](https://github.com/user-attachments/assets/c65717ad-542d-4c39-847d-c1421a55cb88)

![Example_X](https://github.com/user-attachments/assets/aafb7663-81c1-44f8-a124-2c4642690928)

![Example_Y](https://github.com/user-attachments/assets/06efbb73-b0fb-4d53-8e2e-c123d955c9ad)

![Example_Z](https://github.com/user-attachments/assets/3f3699a3-7867-4a9e-a79c-543477ad29c6)
