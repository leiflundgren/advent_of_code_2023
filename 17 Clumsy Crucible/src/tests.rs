
// Note this useful idiom: importing names from outer (for mod tests) scope.
use super::*;

static INPUT_MAP: &str = r#"
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"#;


#[test]
fn test_parse() {
    let m : Map = parse_map(INPUT_MAP);
    assert!(! n.is_none())
}
