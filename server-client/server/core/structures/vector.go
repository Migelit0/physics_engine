package structures

type Vector struct {
	X, Y float64
}

// Add two vectors
func (v Vector) add(v2 Vector) {
	v.X += v2.X
	v.Y += v2.Y
}

// Multiply vector and coefficient
func (v Vector) mul(k float64) {
	v.X *= k
	v.Y *= k
}

// Divide vector and number
func (v Vector) div(k float64) {
	v.X /= k
	v.Y /= k
}
