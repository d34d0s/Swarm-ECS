# Swarm ECS Specification (2.0.2024)
# Izaiyah (stozak) Stokes 2024

# A Visual Representation of An EntityID for Entity=0 With 0 Components attached
#  0 0 0 0  0 0 0 0   0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0
# |--nComponents--|   |-----------------------------EntityID-------------------------------|
# upper bit-range                                                            lower bit-range

from collections import Counter

NID_STRIDE = 0b1000     # Number of bits for the number of components
CID_STRIDE = 0b10000    # Number of bits for each Component ID
EID_STRIDE = 0b100000   # Number of bits for the Entity ID

__EID_COUNT:Counter=Counter()
def gen_entity() -> int:
    EID = __EID_COUNT['EID']
    __EID_COUNT['EID'] += 1; return EID

def unpack_EID(EID: int) -> tuple[int, int, list[int]]:
    # Extract the entity ID from the lower 32 bits
    U_EID = EID & ((1 << EID_STRIDE) - 1)
    
    # Extract the number of components from the next 8 bits
    U_NID = (EID >> EID_STRIDE) & ((1 << NID_STRIDE) - 1)
    
    # Extract each component ID
    FULL_STRIDE = EID_STRIDE + NID_STRIDE
    U_CID = []
    for _ in range(U_NID):
        CID = (EID >> FULL_STRIDE) & ((1 << CID_STRIDE) - 1)
        U_CID.append(CID)
        FULL_STRIDE += CID_STRIDE

    return U_EID, U_NID, U_CID

def pack_EID(EID: int, CID: list[int]) -> int:
    U_EID, U_NID, U_CID = unpack_EID(EID)
    if U_NID > 0:
        for C in U_CID:
            CID.append(C)

    if len(CID) > (1 << NID_STRIDE) - 1:
        raise ValueError("Too many components to pack.")
    
    P_EID = U_EID
    
    # Pack the number of components into the next 8 bits
    P_EID |= len(CID) << EID_STRIDE
    
    # Pack each component ID into the remaining bits
    FULL_STRIDE = EID_STRIDE + NID_STRIDE
    for C in CID:
        P_EID |= C << FULL_STRIDE
        FULL_STRIDE += CID_STRIDE
    return P_EID

def get_CID(EID: int, CID: int) -> int | None:
    _, _, U_CID = unpack_EID(EID)
    for C in U_CID:
        if C == CID:
            return C
    return None

def has_CID(EID: int, CID: int) -> bool:
    _, _, U_CID = unpack_EID(EID)
    return CID in U_CID

def rem_CID(EID: int, CID: int) -> int:
    U_EID, U_NID, U_CID = unpack_EID(EID)
    if CID not in U_CID:
        return EID  # Return the same data if the component is not found    
    U_CID = [C for C in U_CID if C != CID]
    return pack_EID(U_EID, U_CID)
