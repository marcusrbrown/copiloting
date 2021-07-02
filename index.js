function calculateDatesBetweenBeginAndEnd(begin, end) {
  const beginDate = new Date(begin);
  const endDate = new Date(end);
  const daysBetweenBeginAndEnd = Math.ceil((endDate.getTime() - beginDate.getTime()) / (1000 * 60 * 60 * 24));
  return daysBetweenBeginAndEnd;
}
