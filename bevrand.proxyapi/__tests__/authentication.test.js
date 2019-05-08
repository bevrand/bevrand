function add(a , b) {
  return a + b;
}

describe('This is my beautiful testsuite', () => {
  it('Should export a function', () => {
    expect(add(1, 2)).toBe(3);
  })
});
