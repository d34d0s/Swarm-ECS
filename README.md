# Swarm-ECS Specification

## Overview

The **Swarm 2.0.2024** ECS (Entity Component System) specification defines a compact and efficient method for managing entities and their components in a game or simulation engine. By using bitwise operations, it ensures high performance and flexibility.

## Bit Strides

The specification uses three primary bit strides:

1. **Entity ID (EID) - 32 bits**
2. **Number of Components (NID) - 8 bits**
3. **Component ID (CID) - 16 bits**

### Calculations and Limits

1. **Entity ID (EID) - 32 bits:**
   - **Range:** \(2^{32} = 4,294,967,296\) unique IDs.
   - **Capability:** Up to 4 billion unique entities.

2. **Number of Components (NID) - 8 bits:**
   - **Range:** \(2^8 = 256\) values.
   - **Capability:** Each entity can have up to 255 components (0 indicates no components).

3. **Component ID (CID) - 16 bits:**
   - **Range:** \(2^{16} = 65,536\) unique IDs.
   - **Capability:** Over 65,000 different component types.

## Functions

### `unpack_EID(EID: int) -> tuple[int, int, list[int]]`
Extracts the entity ID, number of components, and component IDs from a packed integer.
- **Parameters:**
  - `EID`: Packed entity data.
- **Returns:**
  - Tuple: `(Entity ID, Number of Components, List of Component IDs)`

### `pack_EID(EID: int, CID: list[int]) -> int`
Packs an entity ID and its component IDs into a single integer.
- **Parameters:**
  - `EID`: Base entity ID.
  - `CID`: List of component IDs to attach.
- **Returns:**
  - Packed entity data.

### `get_CID(EID: int, CID: int) -> int | None`
Retrieves a specific component ID from packed entity data.
- **Parameters:**
  - `EID`: Packed entity data.
  - `CID`: Component ID to find.
- **Returns:**
  - The component ID if found, otherwise `None`.

### `has_CID(EID: int, CID: int) -> bool`
Checks if a specific component ID exists in the packed entity data.
- **Parameters:**
  - `EID`: Packed entity data.
  - `CID`: Component ID to check.
- **Returns:**
  - `True` if the component ID exists, otherwise `False`.

### `rem_CID(EID: int, CID: int) -> int`
Removes a specific component ID from the packed entity data.
- **Parameters:**
  - `EID`: Packed entity data.
  - `CID`: Component ID to remove.
- **Returns:**
  - Updated packed entity data.

## Example Usage

```python
EID = gen_entity()
EID = pack_EID(EID, [123, 456, 789, 12345])
print(f"Packed Data: {EID}")

EID = pack_EID(EID, [6789])
print(f"Packed Data: {EID}")

EID = pack_EID(EID, [1324])
print(f"Packed Data: {EID}")

unpacked_EID, n_components, unpacked_CIDs = unpack_EID(EID)
print(f"Unpacked EID: {unpacked_EID}, Unpacked NID: {n_components}, Unpacked CIDs: {unpacked_CIDs}")

print(f"Has Component 456: {has_CID(EID, 456)}")
print(f"Get Component 12345: {get_CID(EID, 12345)}")

EID = rem_CID(EID, 12345)
print(f"Packed Data after removing Component 12345: {EID}")
unpacked_EID, n_components, unpacked_CIDs = unpack_EID(EID)
print(f"Unpacked EID: {unpacked_EID}, Unpacked NID: {n_components}, Unpacked CIDs: {unpacked_CIDs}")

EID = rem_CID(EID, 6789)
print(f"Packed Data after removing Component 6789: {EID}")
unpacked_EID, n_components, unpacked_CIDs = unpack_EID(EID)
print(f"Unpacked EID: {unpacked_EID}, Unpacked NID: {n_components}, Unpacked CIDs: {unpacked_CIDs}")
```

---

## How It Works

### Memory Layout

1. **Entity ID (EID) - 32 bits:**
   - **Range:** \(2^{32}\), allowing for over 4 billion unique entities.
   - **Purpose:** Uniquely identifies each entity.

2. **Number of Components (NID) - 8 bits:**
   - **Range:** \(2^8\), allowing up to 255 components (0 indicates no components).
   - **Purpose:** Specifies how many components are associated with the entity.

3. **Component ID (CID) - 16 bits:**
   - **Range:** \(2^{16}\), permitting over 65,000 unique component IDs.
   - **Purpose:** Identifies each component type attached to the entity.

### Memory Efficiency

- **Compact Representation:** 
  - Multiple pieces of information are packed into a single 64-bit integer, minimizing memory overhead. This approach reduces the need for separate data structures.

- **Fast Access and Manipulation:**
  - **Bitwise Operations:** Efficiently extract and pack data using bitwise operations. These operations are fast, crucial for performance in applications with many entities.
  - **Direct Indexing:** Allows for quick lookups and updates, such as checking if an entity has a specific component.

### Why It’s Powerful

1. **Scalability:** 
   - Handles a vast number of entities and components, with 4 billion entity IDs and 65,000 component IDs, ensuring the system can scale.

2. **Performance:**
   - **Memory Access:** Reduces cache misses and improves memory access patterns by storing all data in a single integer.
   - **Processing Speed:** Fast bitwise operations make data manipulation efficient.

3. **Flexibility:**
   - Customizable bit strides allow adaptation to different needs by adjusting the allocation of bits for entities and components.

4. **Easy Extension:**
   - Adding new components or entities involves simple changes to bit allocation, avoiding complex data structure overhauls.

### Example in Practice

In a game with thousands of entities, each having various components (e.g., `Position`, `Velocity`, `Health`, `Inventory`), the Swarm-ECS specification enables efficient storage and quick updates. For instance, checking if an entity has a `Health` component is a fast bitwise operation, avoiding complex searches.

## Summary

The Swarm-ECS specification provides a highly efficient way to manage entities and components, leveraging bitwise operations for compact representation, fast access, and scalability. It’s particularly well-suited for performance-critical applications such as games and simulations.

---