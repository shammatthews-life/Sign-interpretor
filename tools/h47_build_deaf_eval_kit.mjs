/**
 * Builds a genuine, unfabricated Deaf-Centred Comprehension Evaluation Pack
 * (artifacts/h47/deaf_eval_kit/eval_protocol_pack.json) for future ISL reviewer sessions.
 *
 * Includes:
 *  - Blinded, randomized trial items drawn from locked Videos A & B + minimal-pair NMM/spatial contrasts
 *  - Meaning reconstruction prompts + 4-option semantic distractor multiple choice (1 target + 3 plausible distractors)
 *  - Confidence (1-5), Naturalness (1-5), Visual Readability (1-5), and Open Feedback fields
 *  - Zero fabricated participant responses (status: READY_FOR_DEAF_PARTICIPANT_RECRUITMENT)
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const outDir = path.join(ROOT, 'artifacts/h47/deaf_eval_kit');
fs.mkdirSync(outDir, { recursive: true });

const pack = {
  schema_version: '1.0.0',
  milestone: 'H47',
  status: 'READY_FOR_DEAF_PARTICIPANT_RECRUITMENT',
  fabricated_participants: false,
  participants_recruited: 0,
  design: {
    blind_to_source_text: true,
    counterbalanced_order: ['block_A_comprehension', 'block_B_minimal_pairs', 'block_C_continuous_clips'],
    max_session_minutes: 35,
    consent_modality: 'ISL_video_plus_plain_text_summary',
    scales: {
      confidence: '1 (Guessing) to 5 (Completely Certain)',
      naturalness: '1 (Robotic/Unnatural) to 5 (Natural ISL)',
      readability: '1 (Hands/Face Unreadable) to 5 (Very Clear)'
    }
  },
  trials: [
    {
      trial_id: 'TRIAL-01',
      source_ref: 'MXKkXXYUxBc:A02',
      task_type: 'meaning_reconstruction_and_mc',
      stimulus_video_clip: 'artifacts/h46/recordings/h46_video_a_recording.mp4#t=8.45,14.45',
      blind_prompt: 'Watch the avatar clip (no captions). In your own words (ISL video or text), what is the signer saying?',
      mc_question: 'Which English meaning best matches what the avatar signed?',
      options: [
        { id: 'A', role: 'target', text: 'To help you overcome feeling uncertain, nervous, anxious, or afraid.' },
        { id: 'B', role: 'lexical_distractor', text: 'To ask you why you left the meeting room early.' },
        { id: 'C', role: 'polarity_distractor', text: 'You cannot overcome feeling nervous or afraid.' },
        { id: 'D', role: 'role_distractor', text: 'They helped the teacher prepare the public video.' }
      ]
    },
    {
      trial_id: 'TRIAL-02',
      source_ref: 'y8tFSuOMAqQ:B15',
      task_type: 'meaning_reconstruction_and_mc',
      stimulus_video_clip: 'artifacts/h46/recordings/h46_video_b_recording.mp4#t=50.0,55.0',
      blind_prompt: 'Watch the avatar clip (no captions). Describe who is doing what and whether it is positive or negative.',
      mc_question: 'Which meaning matches the avatar clip?',
      options: [
        { id: 'A', role: 'target', text: 'The problem is not that you do not know; you need to find a story.' },
        { id: 'B', role: 'polarity_distractor', text: 'The problem is that you know everything already.' },
        { id: 'C', role: 'lexical_distractor', text: 'Everyone liked the music in the first scene.' },
        { id: 'D', role: 'wh_distractor', text: 'Who told you where the camera is?' }
      ]
    },
    {
      trial_id: 'TRIAL-03',
      source_ref: 'H47-MINIMAL-NMM-01',
      task_type: 'nmm_minimal_pair_discrimination',
      blind_prompt: 'Two clips use the same manual signs (YOU HELP). Decide which is a statement, which is a negative, and which is a question.',
      pairs: [
        { clip_id: 'A', condition: 'affirmative_neutral', nmm: [] },
        { clip_id: 'B', condition: 'negation_headshake', nmm: ['NMM-NEG-HEADSHAKE'] },
        { clip_id: 'C', condition: 'yesno_brow_raise', nmm: ['NMM-YESNO-BROW-RAISE'] }
      ]
    },
    {
      trial_id: 'TRIAL-04',
      source_ref: 'H47-SPATIAL-LOCUS-01',
      task_type: 'spatial_agent_patient_identification',
      blind_prompt: 'Watch the avatar sign about two people (left vs right). Who helped whom?',
      mc_question: 'Which direction of help did the avatar show?',
      options: [
        { id: 'A', role: 'target', text: 'Person on the left helped person on the right.' },
        { id: 'B', role: 'reversal_distractor', text: 'Person on the right helped person on the left.' },
        { id: 'C', role: 'neutral_distractor', text: 'Nobody helped anyone.' },
        { id: 'D', role: 'unsure', text: 'Could not tell from the avatar movement.' }
      ]
    }
  ]
};

const outPath = path.join(outDir, 'eval_protocol_pack.json');
fs.writeFileSync(outPath, JSON.stringify(pack, null, 2) + '\n', 'utf8');
console.log(`Generated Deaf-Centred Evaluation Pack (${pack.trials.length} structured blind trials) at ${outPath}`);
