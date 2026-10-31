export function takePendingAetherEvent(pendingEvents, eventId) {
  if (!(pendingEvents instanceof Map)) {
    throw new TypeError('Pending Aether events must be stored in a Map.');
  }
  if (typeof eventId !== 'string' || !eventId) return null;
  const pending = pendingEvents.get(eventId);
  if (!pending) return null;
  pendingEvents.delete(eventId);
  return pending;
}
