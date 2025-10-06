This program converts between **Polar** and **Rectangular** coordinate systems through a user-friendly interface.

## Key Components

### 1. Coordinate Classes
- **`PolarCoordinate`**: Represents coordinates with `distance` and `angle`
- **`RectangularCoordinate`**: Represents coordinates with `northing` and `easting`

### 2. Conversion Functions
- **`polar_to_rect()`**: Converts polar to rectangular coordinates using trigonometric functions
- **`rect_to_polar()`**: Converts rectangular to polar coordinates using Pythagorean theorem and arctangent

### 3. Main Program Flow
- **`collect_coordinates()`**: Gets user input for coordinate type and values
- **`transform_coordinates()`**: Automatically detects input type and performs conversion
- **`start()`**: Entry point that initiates the program

## How It Works

1. **User Input**: Program asks whether input will be Polar or Rectangular coordinates
2. **Data Collection**: User enters multiple coordinate values
3. **Automatic Detection**: Program detects input type and converts to the opposite system
4. **Output**: Results are printed and stored in `output_coordinates` list

## Example Usage

If you input Polar coordinates:
- Input: `distance=5, angle=0.785` (45° in radians)
- Output: `northing≈3.54, easting≈3.54`

If you input Rectangular coordinates:
- Input: `northing=3, easting=4`
- Output: `distance=5, angle≈0.93` (≈53°)

## Strengths

- Clean object-oriented design
- Type hints for better code clarity
- Automatic coordinate system detection
- Handles multiple coordinates at once
- Good separation of concerns

## Potential Improvements

- Add input validation for angles and distances
- Handle edge cases (like zero distance)
- Add option to choose output format (degrees/radians)
- Include error handling for invalid inputs