#include "triangle.h"

/* Constructor */
Triangle::Triangle() {
    p1 = Point();
    p2 = Point();
    p3 = Point();
}
Triangle::Triangle(const Point &p1, const Point &p2, const Point &p3) {
    this->p1 = p1;
    this->p2 = p2;
    this->p3 = p3;
}
Triangle::Triangle(const Triangle &t) {
    p1 = t.getP1();
    p2 = t.getP2();
    p3 = t.getP3();
}

/* Destructor */
Triangle::~Triangle() {
}

/* Getters */
Point Triangle::getP1() const {
    return p1;
}
Point Triangle::getP2() const {
    return p2;
}
Point Triangle::getP3() const {
    return p3;
}
std::ostream &operator<<(std::ostream &os, const Triangle &t) {
    os << std::fixed << std::setprecision(4) << t.getP1() << " -- " << t.getP2() << " -- " << t.getP3();
    return os;
}

/* Setters */
void Triangle::setP1(const Point &p1) {
    this->p1 = p1;
}
void Triangle::setP2(const Point &p2) {
    this->p2 = p2;
}
void Triangle::setP3(const Point &p3) {
    this->p3 = p3;
}
void Triangle::setPoints(const Point &p1, const Point &p2, const Point &p3) {
    this->p1 = p1;
    this->p2 = p2;
    this->p3 = p3;
}
std::istream &operator>>(std::istream &is, Triangle &t) {
    Point p1, p2, p3;
    is >> p1 >> p2 >> p3;
    t.setPoints(p1, p2, p3);
    return is;
}

/* Functions */
double Triangle::perimeter() const {
    // TODO: Return the perimeter of the triangle
    double l1 = p1.distance(p2);
    double l2 = p2.distance(p3);
    double l3 = p3.distance(p1);
    double perimeter = l1 + l2 + l3;
    return perimeter;
    return 0;
}
double Triangle::area() const {
    // TODO: Return the area of the triangle
    double l1 = p1.distance(p2);
    double l2 = p2.distance(p3);
    double l3 = p3.distance(p1);
    double  s = (l1 + l2 + l3)/2;  // Semiperimeter
    double area = std::sqrt(s*(s-l1)*(s-l2)*(s-l3)); // Heron’s formula
    return area;
    return 0;
}
