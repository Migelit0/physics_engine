package structures

type Body struct {
	id      uint16
	X, Y    float64
	mass    float64
	speedUp Vector
	speed   Vector
}

func (b Body) updateCoords() {
	b.X += b.speed.X
	b.Y += b.speed.Y
}

func (b Body) updateSpeed() {
	b.speed.add(b.speedUp)
}
