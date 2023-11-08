# Control

- Use Left or Right Arrow key to rotate the robot arms.
- Use the Space key to close and open the gripper.

# Explanation

1. Import necessary libraries: Pygame for graphics and NumPy for mathematical operations.
2. Define constants for colors and window dimensions.
3. Implement functions `Rmat` and `Tmat` for calculating rotation and translation matrices.
4. Create a function `draw` to draw polygons on the screen with proper transformations.
5. In the `main` function, define variables for arm segment angles and gripper control.
7. Handle keyboard input for changing arm angles using Left and Right Arrow keys.
9. Toggle the gripper open and closed using the Space key.
10. Ensure that joint angles are within their respective limits.
11. Draw the robot arm and gripper with the updated angles.
