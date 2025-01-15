# include "linked_list.h"
# include <iostream>
# include <string>

using std::cout, std::endl, std::string, std::ostream;

void MyList::add(const std::string& name, int score) {
    MyNode* newNode = new MyNode(name, score);
    
    if (_tail) {
        newNode->prev = _tail;
        _tail->next = newNode;
    } else {
        _head = newNode; // First node in the list
    }
    _tail = newNode;
    ++_size; // Increment size
}

void MyList::clear() {
    MyNode* current = _head;
    while (current != nullptr) {
        MyNode* temp = current;
        current = current->next;
        delete temp;
    }
    _head = nullptr;
    _tail = nullptr;
    _size = 0; // Reset size
}

bool MyList::remove(const std::string& name) {
    // TODO
   
    return false;
}

bool MyList::insert(const std::string& name, int score, size_t index) {
    // TODO
    // MyNode* newNode = new MyNode(name, score);
    // for (MyNode* myPtr = this->_tail; _tail != nullptr; myPtr = myPtr->next){
    //     if (myPtr->name == name){
    //         MyNode* temp = myPtr->next;
    //         myPtr->next = myPtr->prev;
    //         myPtr->prev = temp;
    //         delete temp;
    //     }

    // }
    return false;
}

MyList::MyList() : _size(0), _head(nullptr), _tail(nullptr) {}

MyList::~MyList() {
    clear();
}

size_t MyList::size() const {
    return _size;
}

bool MyList::empty() const {
    return _head == nullptr;
}

MyNode* MyList::head() const {
    return _head;
}

ostream& operator<<(ostream& os, const MyList& myList) {
    MyNode* _current = myList.head();
    if (_current == nullptr) {
        os << "<empty>" << endl;
        return os;
    }

    os << "[ " << _current->name << ", " << _current->score << " ]";
    _current = _current->next;
    while (_current != nullptr) {
        os << " --> [ " << _current->name << ", " << _current->score << " ]";
        _current = _current->next;
    }
    
    return os;
}

MyNode::MyNode(const std::string& name, int score) : name{name}, score{score}, next{nullptr}, prev{nullptr} {}
