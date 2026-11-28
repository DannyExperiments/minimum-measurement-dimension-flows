import Std

namespace FlowPerturbation
/-- Multiply a signed combination of the r perturbations by 4^r.
Taking the last coefficient modulo 4 successively recovers each digit. -/
def numerator : List Int → Int
  | [] => 0
  | d :: ds => d + 4 * numerator ds
def Digits (ds : List Int) := ∀ d ∈ ds, d = -1 ∨ d = 0 ∨ d = 1
/-- Read the lowest base-four digit modulo four, then recurse on the
shorter list. This also covers lists with leading zero digits. -/
theorem zero_iff (ds : List Int) (h : Digits ds) :
    numerator ds = 0 ↔ ∀ d ∈ ds, d = 0 := by
  induction ds with
  | nil => simp [numerator]
  | cons a ds ih =>
    constructor
    · intro eqn
      have ha := h a (by simp)
      change a + 4 * numerator ds = 0 at eqn
      have ha0 : a = 0 := by
        rcases ha with ha | ha | ha <;> omega
      have ht : numerator ds = 0 := by omega
      intro d hd
      rcases List.mem_cons.mp hd with hd | hd
      · exact hd.trans ha0
      · exact (ih (fun j hj => h j (by simp [hj]))).mp ht d hd
    · intro allzero
      rw [show a = 0 from allzero a (by simp)]
      simp [numerator, (ih (fun j hj => h j (by simp [hj]))).mpr (fun j hj => allzero j (by simp [hj]))]
#print axioms zero_iff
end FlowPerturbation
